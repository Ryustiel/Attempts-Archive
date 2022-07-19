"""
indiquer "":"#variables" dans meta pour que la node soit nommee avec le nom de l'interface 
"""

from graphviz import Digraph
from utilities import JsonInterface
import importlib.util

meta = JsonInterface("meta.json").get()
processes = JsonInterface("desc.json").get()
del processes[""]

graph = Digraph(format='pdf')

graph.node("REPEAT", "REPEAT", color='red', fontcolor='red', fontstyle='bold')

for name, properties in processes.items():
    display_name = name
    color = 'gray'
    style='dashed'

    #color
    if len(properties['Output']) == 0:
        color = 'magenta'
        style='solid'
    else:
        print('OUTPUT', properties['Output'])
        for values in properties['Output'].values():
            if 'REPEAT' in values:
                color = 'green'
                style='solid'
                break 
    if color == 'gray' and name[-1] == '.':
        color = 'darkmagenta'
        style='solid'

    #interfaces
    if len(properties['Interfaces']) > 0:
        display_name += '\n['
        first = True
        for interface in properties['Interfaces']:
            if first:
                first = False 
            else:
                display_name += ', '
            display_name += interface
        display_name += ']'

    graph.node(name, display_name, color=color, style=style)

    #edge to interface event
    for target_interface in properties['Interfaces']:
        for interface in meta['interfaces']:
            if interface['name'] == target_interface:
                graph.edge(name, interface['name'], color='orange', style='solid')
                break 

    #edges
    for output_name, destinations in properties['Output'].items():
        
        for destination in destinations:

            style='solid'
            connection_color = 'gray'

            if output_name == 'ExpectIfYes':
                connection_color = 'gray'
                style='dotted'
            elif output_name == 'ExpectIfNo':
                connection_color = 'gray'
                style='dotted'
            elif output_name == 'Expect':
                connection_color = 'gray'
                style='dotted'
            elif output_name == 'Require':
                connection_color = 'gray'
                style='dashed'
            elif output_name == 'Yes':
                connection_color = 'green'
            elif output_name == 'No':
                connection_color = 'red'

            graph.edge(name, destination, color=connection_color, style=style)

#interfaces et pipelines

for interface in meta['interfaces']:
    for event_name, cascade_list in interface['events'].items():
        
        if event_name == "":
            name = interface['name']
            display_name = name 
        else:
            name = interface['name'] + event_name
            display_name = interface['name'] + " : " + event_name
        
        graph.node(name, display_name, color='orange', style='solid', fontcolor='orange', fontstyle='bold')
        
        for cascade in cascade_list:
            if not cascade == "#variables":
                graph.edge(name, cascade, color='orange', style='solid')
                
            elif interface["name"] == "Spacy Word2Vec":
                sentences = JsonInterface("interfaces/data/word2vec_base_sentences.json") #portee globale dans le module
                reponses = sentences.get()["responses"]
                for response_cascade in reponses.values(): #responses = {id : cascade_name}
                    graph.edge(name, response_cascade, color='gray', style='dashed')


graph.render('graphs/machin', view=True)



#un noeud est une question qu'on peut se poser a soi meme, unique.
#une node traite l'ensemble des cas possibles de la question.

#la node emet des outputs qui seront traites par le truc central.
#cela comprend des Yes No, ExpectIfYes, ExpectIfNo, Expect (systematiquement).

#une node peut executer des methodes d'interfaces, et lancer des pipelines (apres avoir eventuellement pretaite des donnees)