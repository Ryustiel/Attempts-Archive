"""
Manages a scripted conversation to trigger actions

history : data for training future conversation managers
training : input data stored by tag for training current manager : used by the tree system to EXPECT inputs
shortcuts : ensembles of actions (and internal module patterns like "ask for inputs") to be performed following the execution of a node 
tree : stores the tree
"""
from utilities import JsonInterface
import pydot

training_data = JsonInterface("MODULES/conversation/training.json")
shortcuts = JsonInterface("MODULES/conversation/shortcuts.json")
history = JsonInterface("MODULES/conversation/history.json")

def exec_shortcut(meep, shortcut):
    ...
    # recupere un shortcut et l'execute
    for sht, actions in shortcuts.data.items():
        if sht == shortcut:
            for action in actions:
                meep.EXECUTE(action[0], *action[1:])
            return
    
    raise ValueError("No shortcut found for shortcut %s" % shortcut)

class Node:
    def __init__(self, tags, outputs, next):
        self.tags = []
        self.outputs = []
        self.next = []

    def get_training(self):
        training = []
        for tag in self.tags:
            training += training_data.get(tag)
        return training

class Tree:
    """
    THIS STRUCTURE (along with the Nodes class) can be generalized as a tree load/save storage system to be used in other modules.
    gotta be MOVED to utilities.py and modified to implement any kind of similar tree storage. (args like fields must be parameters of Tree __init__)
    """
    def __init__(self, meep=None, path="MODULES/conversation/tree.json"):
        """
        loads the tree first
        creates a new tree if no path
        """
        self.path = path
        self.meep = meep
        self.nodes = []

    def load(self):
        nodes_data = JsonInterface(self.path).get("nodes")
        complete = [] # next attribute full
        pending = [] # 

        for single_node_data in nodes_data: # nodes_data : {tags, outputs, next}
            node = Node(**{single_node_data[key] for key in ["tags", "outputs", "next"]})
            if node.results == []:
                complete.append( (single_node_data["storage_id"], node) )
            else:
                pending.append( (single_node_data["storage_id"], node) )
            self.nodes.append(node)

        # replacing storage_id with pointers 
        limiter = self.single_node_data
        for factorial_number in range(1, len(self.single_node_data)):
            limiter *= factorial_number

        while pending != [] and limiter > 0:
            for i, (storage_id, node) in enumerate(pending): # checks every node
                pending_storage_values = 0 # counts how much storage values are in node.next
                for j, value in enumerate(node.next):
                    if isinstance(value, str): # value is storage_id
                        pending_storage_values += 1 

                        target_storage_id = value
                        for (complete_storage_id, complete_node) in complete:
                            if complete_storage_id == target_storage_id:
                                node.next[j] = complete_node
                                pending_storage_values -= 1 # success

                    # if next is already a pointer, do not increment pending_storage_values, do not look for complete_nodes

                # if that node has no more storage values (only references or empty)
                if pending_storage_values == 0:
                    complete.append(pending.pop(i)) # moves the node from pending to complete
                    break # starts another enumerate cycle

            limiter -= 1 # stops at limiter if worse case scenario steps exceded

        assert pending == []

    def save(self, path=None):
        storage = JsonInterface(self.path)
        count_storage_ids = 0
        identified_node_ids = {} # nodes that already have an id : {node: id}
        storage.data = {"nodes": []}

        for node in self.nodes:
            if not node in identified_node_ids.keys: # adds the node itself
                identified_node_ids[node] = count_storage_ids
                data = {"storage_id": count_storage_ids, "tags": node.tags, "outputs": node.outputs, "next": []} # next will be filled in the next step
                count_storage_ids += 1 
                storage.data += data               

        for node in self.nodes:
            for next in node.next:
                if not next in identified_node_ids.keys():
                    print("WARNING : skipped saving of node (tags: %s) as next node of (tags: %s) because it was not referenced in Tree.nodes" % (next.tags, node.tags))
                else:
                    for i, json_node in enumerate(storage.data["nodes"]):
                        if json_node["storage_id"] == identified_node_ids[next]: # found storage id of next node
                            next_storage_id = identified_node_ids[next]
                            storage.data["nodes"][i]["next"].append(next_storage_id)
                            break
            
        storage.save()

    def add(seld, node):
        ...

    def display(self):
        """
        display function
        """
        graph = pydot.Dot(graph_type='graph')

        for node in self.nodes: # display the tree
            node_graph = pydot.Node(name=str(node.tags))
            graph.add_node(node_graph)
            for next in node.next:
                edge = pydot.Edge(str(node.tags), str(next.tags))
                graph.add_edge(edge)

        graph.write_png('tree.png')

# ============================================================================= DNN

# building training data (--- at least allows for an easy display of what people said to the bot in specific circumstances, to make it easier to add new training data)


# using the model

def train():
    ... # trains the model

    # takes the training data, le format correctement pour l'entraînement, lance l'entraînement

def predict():
    ...

    #exécute la fonction


