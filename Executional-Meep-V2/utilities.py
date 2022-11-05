import json

class JsonInterface:
    def __init__(self, path):
        self.data = {}
        try:
            with open(path, 'r') as f:
                self.load(path)
        except:
            raise ValueError("Could not load JSON file at path '%s'" % path)
        self.path = path
    
    def load(self, path=None):
        if path is None:
            path = self.path
        with open(path, "r", encoding="utf8") as f: #wont work out of windows
            self.data = json.load(f)

    def get(self, *key) -> dict:
        if key:
            return self.data[key[0]]
        return self.data

    def __getitem__(self, key) -> any:
        return self.data[key]

    def update(self, datatype, id, name):
        self.data[datatype].update({str(id):name})
    
    def save(self, path=None):
        if path is None:
            path = self.path
        with open(path, "w", encoding='utf8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)


from difflib import SequenceMatcher

def matching(comparing: str, compare_list: list, min_ratio=0.5):
    """
    compares string to a list of strings and returns the most similar if one is similar enough.
    """
    best = None 
    best_ratio = min_ratio

    for item in compare_list:
        matched = SequenceMatcher(None, comparing, item)
        ratio = matched.ratio()
        if ratio > best_ratio:
            best_ratio = ratio
            best = item

    return best

def matching_name_attribute(comparing, compare_objects_list, min_ratio=0.5):
    """
    compares string to the name of the functions from a list of functions and returns the function with the most similar name, if one is similar enough.
    """
    best = None 
    best_ratio = min_ratio

    for item in compare_objects_list:
        matched = SequenceMatcher(None, comparing, item.__name__)
        ratio = matched.ratio()
        if ratio > best_ratio:
            best_ratio = ratio
            best = item

    return best