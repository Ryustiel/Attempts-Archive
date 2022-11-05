"""
Functions that are useful to a wide range of activites
also serve as a repository for testing functions
"""
import asyncio
from difflib import SequenceMatcher

def similarity(meep, comparing: str, compared:str):
    """
    getter
    compares string to a list of strings and returns the most similar if one is similar enough.
    """
    matched = SequenceMatcher(None, comparing, compared)
    return matched.ratio()

def list_string_matcher(meep, comparing, compare_list, seuil=0.5):
    """
    getter
    compares a string (comparing) to a list of strings "compare_list" and returns a list of these strings ordered by similarity with their similarity scores : [(object, similarity)]
    """

    rankings = [(compare_list[0], similarity(meep, comparing, compare_list[0]))] # similarity scores of functions : (id, score) -- with initial element

    for i in range(1, len(compare_list)):
        unranked_score = similarity(meep, comparing, compare_list[i])
        ranked = False
        for j, (function_string, score) in enumerate(rankings):
            if unranked_score > score:
                rankings.insert(j, (compare_list[i], unranked_score))
                ranked = True 
                break
        if not ranked:
            rankings.append((compare_list[i], unranked_score))

    return rankings

def findthat(meep):
    """
    action
    says something using the talker
    """
    meep.EXECUTE("talker : say", "TEST SUCCESSFUL")

def trytosay(meep):
    """
    action init
    tries something
    """
    meep.EXECUTE("says using the talker")