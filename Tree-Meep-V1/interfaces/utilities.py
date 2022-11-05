from json import load, dump
import importlib.util

class JsonInterface:
    def __init__(self, path):
        self.data = {}
        self.load(path)
        self.path = path
    
    def load(self, path=None):
        if path is None:
            path = self.path
        with open(path, "r", encoding="utf8") as f: #wont work out of windows
            self.data = load(f)

    def get(self) -> dict:
        return self.data

    def update(self, datatype, id, name):
        self.data[datatype].update({str(id):name})
    
    def save(self, path=None):
        if path is None:
            path = self.path
        with open(path, "w", encoding='utf8') as f:
            dump(self.data, f, indent=4, ensure_ascii=False)
    
