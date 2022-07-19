"""
une instance de la memoire, capable de lire, d'ecrire, et de sauvegarder la memoire
"""
from json import load, dump
from time import mktime, gmtime

AVAILABLE_DIVISIONS =  ['working', 'states', 'storage']

class Memory():
    def __init__(self):
        with open("memory/memory.json", "r") as f:
            self.content = load(f) #toutes les operations sont faites sur ce fichier
        with open("memory/bulk_memory.json", "r") as f:
            self.bulk_mem_content = load(f) #toutes les operations sont faites sur ce fichier

    def get(self, division, slot) -> list: #MODIFIER L'ACCES A LA MEMOIRE : LES DIVISIONS NE CONSERVENT PAS LE MEME NOMBRE D'ELEMENTS
        """
        returns date and iterator to optionaly browse through memory, and check if date is old enough
        """
        if division in AVAILABLE_DIVISIONS:
            if slot in self.content[division].keys():
                return self.content[division][slot][1:]
        raise ValueError('Could not find memory slot (coder une bulle pour ca)')

    def get_date(self, division, slot) -> int:
        if division in AVAILABLE_DIVISIONS:
            if slot in self.content[division].keys():
                return self.content[division][slot][0]
        raise ValueError('Could not find memory slot (coder une bulle pour ca)')

    def get_logs(self, start=0, n=100):
        mlen = len(self.content['logs'])
        if not start >= mlen:
            if mlen - start - n > 0:
                stop = start + n
            else: 
                stop = mlen
            logs = self.content['logs'][start:stop]
        return logs

    def log(self, tags, variable):
        """
        logs into memory
        """
        log = {"date":mktime(gmtime()), "tags":tags, "variable":variable}
        self.content["logs"].append(log)

    def update(self, division, slot, content):
        if division in AVAILABLE_DIVISIONS:
            if slot in self.content[division].keys():
                self.content[division][slot].insert(1, content)
                self.content[division][slot][0] = mktime(gmtime())
        raise ValueError('Could not find memory slot (coder une bulle pour ca)')

    def save(self):
        pass 


        