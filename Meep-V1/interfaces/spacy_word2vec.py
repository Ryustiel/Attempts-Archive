"""
cascade renvoie les outputs...
"""
from interfaces.utilities import JsonInterface
from numpy import mean

#decaler les imports
import spacy
spacy_pipeline = spacy.load("fr_core_news_md")

class Word2Vec:
    def __init__(self, meep, spacy_pipeline):
        #json preloading
        self.data = JsonInterface("pipelines/data/word2vec_base_sentences.json") #portee globale dans le module

        #spacy preloading
        self.spacy_pipeline = spacy_pipeline

        self.groups = {}
        self.load_sentences()

    def load_sentences(self):
        #comparison vector preprocessing
        self.groups = {}
        for name, sentences in self.data.get()['groups'].items():
            vectors = []
            for sentence in sentences:
                vector = self.spacy_pipeline(sentence) #du coup pas exactement des vecteurs; objet spacy qui contient plusieurs elements d'analyse
                vectors.append(vector)
            self.groups[name] = vectors

    #processing
    def phrase_proche(self, sentence: str) -> list:
        results = []
        for name, vectors in self.groups.items():
            values = [] #depend du nombre de phrases
            best = -1
            for vector in vectors:
                sentence_vector = nlp(sentence) #vecteur de comparaison
                similarity = sentence_vector.similarity(vector)
                values.append(similarity)

                if similarity > best: #garde trace de la similarite
                    best = similarity

            result = (name, best+mean(values))
            results.append(result)

        #SEUIL MINIMUM POUR SE FAIRE UN AVIS
        best = 0.2
        best_name = "uncertain"
        print(results)
        for name, value in results:
            if value > best:
                best = value
                best_name = name
        
        return best_name

    def retrieve_cascade(self, identifiant):
        return self.data.get()['responses'][identifiant]

    def update(self, group, phrase):
        pass
        self.data.save()


