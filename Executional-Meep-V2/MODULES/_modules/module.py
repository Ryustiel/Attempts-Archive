"""
permet de recuperer les donnees des modules et sur les modules, permet de creer de nouveaux modules
"""

import os
import inspect
import string
from utilities import matching_name_attribute

# variables
ignored_list = ""

# ============================== IMPORT ASSISTANCE

def import_all(meep):
    """
    action
    imports (or refreshes) all modules
    """
    for folder in os.listdir(os.path.join(os.getcwd(), "MODULES")): #ICI ON A : GENERAL IMPORTER FUNCTION - ENV.PROJECT_PATH
        name = str(folder).replace(" ", "_")
        meep.IMPORT(name)

# ============================== GET IMPORT DATA

def modules_list(meep):
    """
    getter
    donne la liste des modules disponibles
    """
    return os.listdir(os.path.join(os.getcwd(), "MODULES"))

def ignored(meep, ignored_string):
    """
    action
    registers ignored functions to string to be called again
    """
    print(ignored_string)
    ignored_list += "\n" + ignored_string

def get_ignored(meep):
    """
    getter
    gets ignored string
    """
    return ignored_list

def get_listeners(meep):
    """
    getter
    returns a list of the listener functions
    """
    l = ""
    for module in meep.modules.values():
        for function in module.__listeners__:
            l += "\n" + function.__name__
    return l + "\n"

def get_init(meep):
    """
    getter
    returns a list of the init functions
    """
    l = ""
    for function in meep.init_actions:
        l += "\n" + function.__name__
    return l + "\n"

# ============================== FUNCTION DATA GETTERS

def get_function_category(meep, function):
    """
    getter
    returns the category attribute of the function
    """
    if isinstance(function, str):
        function = get_function_from_instruction_string(meep, function)
    return function.__category__

def get_function_from_instruction_string(meep, instruction):
    """
    getter
    returns the function using its instruction string
    """
    if ":" in instruction:
        s = instruction.split(" : ")
        module = s[0]
        fname = s[1]

        if module == "any": # search through every module
            flist = []
            for mod in meep.modules.values():
                flist.join([f for f in mod.__actions__ + mod.__getters__ + mod.__listeners__])
            function = matching_name_attribute(fname, flist)
        else:
            mod = matching_name_attribute(module, meep.modules.values())
            if mod is not None:
                function = matching_name_attribute(fname, mod.__actions__ + mod.__getters__ + mod.__listeners__)

        if function is None:
            if module == "any":
                raise ValueError('No such module "%s"' % module)
            raise ValueError('No action "%s" found in module "%s"' % (fname, module))
        
        return function
    else:
        raise ValueError('instruction "%s" is not properly formatted to be used in get_function_from_instruction_string (sould be "module : function")' % instruction)

# ============================== FUNCTION DOC OPTIONS

def generate_option_list(meep, category):
    """
    getter
    gets the function string list
    returns (function_list, function_strings_list)
    """
    function_option_string_list = []
    for module in meep.modules.values():
        if category == "getters":
            functions = module.__getters__
        elif category == "actions":
            functions = module.__actions__
        else:
            functions = module.__getters__ + module.__actions__

        for function in functions:
            function_option_string_list.append(generate_function_string(meep, function, module_name=module.__name__))

    return function_option_string_list
        
def generate_option_string(meep, category=""):
    """
    getter
    gets the great option string
    a string that lists every single function in the system
    """
    option_string = ""
    for module in meep.modules.values():
        if category == "getters":
            functions = module.__getters__
        elif category == "actions":
            functions = module.__actions__
        else:
            functions = module.__getters__ + module.__actions__

        for function in functions:
            option_string += generate_function_string(meep, function, module_name=module.__name__) + "\n\n"
    return option_string

def generate_function_string(meep, function, module_name="any"):
    """
    getter
    generate a string representation of a single function (its docstring, name, and module)
    """
    return module_name + " : " + function.__name__ + "|" + function.__doc__ + " parameters : " + str(function.__code__.co_varnames)

def get_parameter_list(self, function):
    """
    getter
    returns the list of the parameters of the function
    the function parameter must be either a function or function string
    """
    if isinstance(function, str):
        i = 2
        parameters_list = []
        try:
            while function[-i] != "(":
                parameters_list.append(function[-i])
        except IndexError as e:
            raise ValueError("Could not extract function parameters : %s" % e)
    else:
        parameters_list = list(function.func_code.co_varnames) # list() to keep the return type unique

    return parameters_list

# ============================== 