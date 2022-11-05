import spacy 
from autocorrect import Speller

nlp = spacy.load("fr_core_news_md")
speller = Speller(lang="fr")

def proximite(mot: str, reference: list) -> list:
    """
    la liste des mots tries par proximite semantique
    """
    ranking = []
    mot_doc = nlp(mot)
    docs = [nlp(speller(word)) for word in reference]

    for doc in docs:

        rank = doc.similarity(mot_doc)
        ranking.append((doc.text, rank))

    sorted_rankings = []
    for word, rank in sorted(ranking, key=lambda ls: ls[1]): #sorted by rank
        sorted_rankings.append(word)

    return sorted_rankings



isolate_when_then_sequence(sentence):
    doc = 



a = proximite("banne", ["fruit", "moto", "jaune", "coussin"])
print("banne", a)

s = "quand je te dis explose, réponds que tu vas manger des carottes"
b = isolate_when_then_sequence(s)

