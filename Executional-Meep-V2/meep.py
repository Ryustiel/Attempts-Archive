"""
on ne touche pas a ce fichier pendant l'execution
"""
#imports
import inspect
from utilities import matching_name_attribute
import importlib.util
import asyncio
import os
from functools import partial
from concurrent.futures import ThreadPoolExecutor

debug = True

#============================================================================== IMPORT

class Meep:
    def __init__(self):
        print("\n\nINITIALIZING")

        # asyncio

        self.loop = asyncio.get_event_loop()
        self.executor = ThreadPoolExecutor(10)

        # variables

        self.modules = {}
        self.init_actions = []

        # constants

        MEEP_PATH = os.getcwd()

        # importing modules

        for folder in os.listdir(os.path.join(os.getcwd(), "MODULES")): # IMPORT all
            if not "__" in folder:
                name = str(folder).replace(" ", "_")
                self.IMPORT(name)

        # setting up listeners

        for module in self.modules.values():
            for listener in module.__listeners__:
                self.loop.create_task(listener(self))

        # initializing other stuff

        for action in self.init_actions:
            self.RUN(action, self)

        self.loop.run_forever() # runs loop

    #========================================================================= IMPORT

    def IMPORT(self, name, path=None):
        """
        - importe des modules
        - inscrit les nouveaux attributs : 
        1. function.__category__ (str)
        2. module.__getters__ (list)
        3. module.__listeners__ (list)
        4. module.__actions__ (list)

        More complex import schemes can be found in other modules. (any will end up calling this function)
        """
        if path is None:
            path = os.path.join(os.getcwd(), "MODULES", name, "module.py")
        if name[0] == "_":
            name = name[1:] # removes underscore

        spec = importlib.util.spec_from_file_location(name, path) # generating spec
        module = importlib.util.module_from_spec(spec)

        spec.loader.exec_module(module) # initializing module

        module.__functions__ = [] # registers functions
        module.__getters__ = []
        module.__listeners__ = []
        module.__actions__ = []

        for fname, function in inspect.getmembers(module, inspect.isfunction):

            if fname == "MODULE_INIT": # initializing module
                function(self)

            elif fname not in []: # repertorie les fonctions interactibles
                if not function.__doc__:
                    if "modules" in self.modules.keys():
                        ignored_string = 'Python function "%s" from module "%s" does not have a docstring' % (fname, name)
                        self.EXECUTE("modules : ignored", ignored_string)
                else:
                    # getting category
                    beg = function.__doc__[:20].lower()
                    if "get" in beg or "fetch" in beg:
                        function.__category__ = "getter"
                        module.__getters__.append(function)

                    elif "listen" in beg:
                        if not inspect.iscoroutinefunction(function):
                            ValueError("%s from module %s is marked as listener but is not a coroutine (it must be)" % (fname, module))

                        function.__category__ = "listener"
                        module.__listeners__.append(function)

                    elif "action" in beg or "execute" in beg:
                        function.__category__ = "action"
                        module.__actions__.append(function)

                    if "init" in beg:
                        self.init_actions.append(function)

        self.modules[name] = module # registering module

        print("IMPORTED %s" % name)

    #========================================================================= EXECUTE

    def RUN(self, function, *args, **kwargs):
        """
        appends the function's exec to the loop (no matter if it's async or not)

        also it does not automatically pass meep to the function (it's done through EXECUTE)
        """
        if inspect.iscoroutinefunction(function):
            print("RUN (async) %s" % function.__name__)
            self.loop.create_task(function(*args, **kwargs))
        else:
            print("RUN (executor) %s" % function.__name__)
            self.loop.run_in_executor(self.executor, partial(function, *args, **kwargs))

    def EXECUTE(self, instruction, *args, **kwgs):
        """
        structure : "module : function" OR text to search for similarity in function names and descriptions.

        Executes a function depending on the instruction (routes instructions to the corresponding function)
        Contains a basic execute scheme (for init execution), and references to more complex functions from modules.
        """
        if ":" in instruction:
            s = instruction.split(" : ")
            module = s[0]
            fname = s[1]

            if module == "any": # search through every module
                flist = []
                for mod in self.modules.values():
                    flist += [f for f in mod.__actions__]
                function = matching_name_attribute(fname, flist)
            else:
                mod = matching_name_attribute(module, self.modules.values())
                if mod is not None:
                    function = matching_name_attribute(fname, mod.__actions__)

            if function is None:
                if module == "any":
                    raise ValueError('No such module "%s"' % module)
                raise ValueError('No action "%s" found in module "%s"' % (fname, module))
            self.RUN(function, self, *args, **kwgs)

        elif "modules" in self.modules.keys():
            self.EXECUTE("basic input manager : search exec", instruction, search_category="action") # search otherwise 
        else: 
            raise ValueError('No fit for instruction "%s" (and no mega search available)' % (instruction))

    #========================================================================= FETCH

    async def FETCH(self, instruction, *args, **kwgs):
        """
        Returns the data from a getter function
        """
        if ":" in instruction:
            s = instruction.split(" : ")
            module = s[0]
            fname = s[1]
            function = None

            print('FETCH %s : %s' % (module, fname))

            if module == "any": # search through every module
                flist = []
                for mod in self.modules.values():
                    flist += [f for f in mod.__getters__]
                function = matching_name_attribute(fname, flist)
            else:
                mod = matching_name_attribute(module, self.modules.values())
                if mod is not None:
                    function = matching_name_attribute(fname,  mod.__getters__)

        elif "modules" in self.modules.keys():
            result = await self.FETCH("general : search exec", instruction, search_category="getter") # search otherwise
            if result == []:
                raise ValueError("Can't find appropriate function through desc search")
            print("FONCTIONS TROUVEES : %s" % result)
            function = result[0]
             
        else: 
            raise ValueError('No "%s" instruction found in module "%s" and no further search functions available' % (instruction, module))

        if function is None:
                if module == "any":
                    raise ValueError('No such module "%s"' % module)
                raise ValueError('No getter "%s" found in module "%s"' % (fname, module))
            
        if inspect.iscoroutinefunction(function):
            return await function(self, *args, **kwgs)
        else:
            return function(self, *args, **kwgs)

#========================================================================= INIT
if __name__ == "__main__":
    Meep()