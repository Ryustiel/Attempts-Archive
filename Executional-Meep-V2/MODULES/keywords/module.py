"""
stores strings of data to get back later (on demand)
"""
from utilities import JsonInterface

data = JsonInterface("MODULES/memo/data.json") # strings : {"id": "content"}

def store(meep, keyword, string_):
    ...