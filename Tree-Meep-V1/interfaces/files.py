import pathlib
from graphviz import Graph

main_path = __file__ 
for _ in range(2):
    main_path = pathlib.Path(main_path).parent.resolve()
print("file", main_path)

graph = Graph(format='jpg')

def list_dir(graph, path: pathlib.Path, parent_node=None):
    if path.is_dir():
        subs = path.iterdir()
        for sub in subs:
            color = 'gray'
            if ".py" in sub.name:
                color = 'blue'
            elif ".json" in sub.name:
                color = 'orange'
            elif ".pdf" in sub.name or ".jpg" in sub.name or ".png" in sub.name or ".txt" in sub.name:
                color = 'black'

            style="solid"
            if color == 'gray':
                style = "dashed"
            
            graph.node(sub.name, sub.name, color=color, style=style)

            if parent_node and not "__" in sub.name:
                graph.edge(parent_node, sub.name, color='gray', style='dashed')
            
            sub_path = pathlib.Path(sub)
            if sub_path.is_dir() and not "__" in sub.name:
                list_dir(graph, sub_path, parent_node=sub.name)

list_dir(graph, pathlib.Path(main_path))
graph.render('graphs/folderview', view=True)