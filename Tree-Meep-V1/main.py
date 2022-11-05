import asyncio
import processes
import importlib.util
from memory.access import Memory
from json import load

def get_processes() -> dict:
    with open("desc.json", "r", encoding="utf-8") as f:
        desc = load(f)
    return desc

async def init_interface(meep, name, path, classname):
    """
    importe et lance les mainloops des interfaces
    """
    print("=================================================> PRINT", name, path, classname)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)

    spec.loader.exec_module(module)
    interface = getattr(module, classname)(meep) #getting interface instance
    meep.loop.create_task(interface.start()) #starting interface
    return interface

class Meep:
    def __init__(self, init_names: list):
        self.mem = Memory()
        self.desc = get_processes()
        self.loop = asyncio.get_event_loop()
        self.interfaces = {}
        self.init_names = init_names

        self.stop = False

    def start(self):
        self.loop.run_until_complete(self.running())

    async def running(self):
        for name in self.init_names:
            self.cascade(name) #eventually completes with a chain of create tasks

        #loops through meta file to get path/class_name
        with open("meta.json", "r") as f:
            meta = load(f)
        for entry in meta['interfaces']:
            name, path, classname, _ = entry.values()
            interface_reference = await init_interface(self, "interfaces."+name, path, classname)
            self.interfaces[name] = interface_reference
        
        channels = self.interfaces["Discord"].identifiers.get()["text channels"]
        self.interfaces["Discord"].send("Union Terrible des Copains (UTC)#général", "thest")

        #timeout
        for c in range(100):
            print(f'counting...{c}')
            await asyncio.sleep(3)
            if self.stop:
                break
        print('fini')

    def queue(self, coroutine, output_schemes: dict) -> None:
        """
        genere une coroutine en recuperant la fonction correspondant a name dans processes
        et insert la coro dans le mainloop 
        (a ce stade la on est deja sur que la fonction existe)
        """
        async def wrapped_coroutine():
            """
            execute la coroutine 
            et lance cascade pour les 'nexts' (coroutines subsequentes) qui correspondent a l'output.
            """
            outputs = await coroutine(self)
            if outputs is not None:
                for output in outputs:
                    for scheme_name, nexts in output_schemes.items(): #nexts : list of function_names
                        if scheme_name == output:
                            if scheme_name == 'Expect':
                                pass #implementation du systeme de priorites
                            else:
                                for next in nexts:
                                    self.cascade(next)

        self.loop.create_task(wrapped_coroutine())

    def cascade(self, name: str) -> None:
        """
        gere l'execution 'en cascade' des bulles. (en simultane; attend la sortie avant d'engendrer l'execution du reste)
        """
        print("CASCADE TRIGGER : "+name)
        if name == "REPEAT":
            print('gonna REPEAT') #repetition de l'antecedant
        elif name in self.desc.keys():
            function_name = self.desc[name]['Function']

            if function_name == '': #nom de fonction indefinie
                self.mem.log(['main', 'pas de fonction'], name)
                self.cascade("dire qu'il n'y a pas de fonction")

            elif not function_name in dir(processes): #correspondance entre desc et processes.py
                raise ValueError(f"Structure du fichier processes.py : la fonction ''{function_name}'' est appellee mais n'est pas definie")

            else: #lancement de la fonction et execution des outputs
                schemes = self.desc[name]['Output']
                coro = getattr(processes, function_name)
                self.queue(coro, schemes)
        else:
            raise ValueError(f"Structure du fichier desc.json : la commande ''{name}'' est appelee mais n'est pas definie")


init_names = []
meep = Meep(init_names)
meep.start()