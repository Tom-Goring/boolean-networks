"""A simple module to create and evaluate given boolean networks up to a certain time step"""

from collections import defaultdict
from typing import Callable


class BooleanNetwork:
    """ Data stucture holding a dict of labels -> nodes and a dict of nodes -> sets of nodes """

    def __init__(self, nodes, connections):
        self._graph = defaultdict(set)
        self._nodes = {}
        for (label, node) in nodes:
            self._nodes[label] = node
        self.add_connections(connections)

    def add_connections(self, connections):
        """ Add connections (list of tuple pairs) to graph """
        for node1, node2 in connections:
            self.add(node1, node2)

    def add(self, node1, node2):
        """ Add connection between node 1 and node 2 """
        self._graph[node1].add(node2)

    def remove(self, node):
        """ Remove all references to node """
        for _, connections in self._graph.items():
            try:
                connections.remove(node)
            except KeyError:
                pass
        try:
            del self._graph[node]
        except KeyError:
            pass

    def step(self):
        """ Increment the current state to the next time step """
        new_nodes = {}
        for (label, node) in self._nodes.items():
            input_nodes = [self._nodes[k] for (k, v) in self._graph.items() if label in v]
            new_node = node.update((input_nodes[0].state, input_nodes[1].state))
            new_nodes[new_node.label] = new_node
        self._nodes = new_nodes

    def __str__(self):
        return "".join(f"{node}, " for node in self._nodes.values())

    def __repr__(self):
        return "".join(f"{node}, " for node in self._nodes.values())


class Node:
    """ Boolean node in network """
    def __init__(self, label: int, state: int, function: Callable[[int, int], int]):
        self.state = state
        self.function = function
        self.label = label

    def update(self, inputs):
        """ Return newly updated node using function applied to inputs (a tuple of integers) """
        return Node(self.label,  self.function(inputs[0], inputs[1]), self.function)

    def __str__(self):
        return f"{self.label}={self.state}"

    def __repr__(self):
        return f"{self.label}={self.state}"


if __name__ == '__main__':
    node_1 = Node(1, 1, lambda x, y: x and y)
    node_2 = Node(2, 1, lambda x, y: x or y)
    node_3 = Node(3, 0, lambda x, y: x or y)
    node_4 = Node(4, 0, lambda x, y: x and y)

    network = BooleanNetwork([
        (node_1.label, node_1),
        (node_2.label, node_2),
        (node_3.label, node_3),
        (node_4.label, node_4)], [
        (1, 2),
        (1, 3),
        (1, 4),
        (2, 1),
        (2, 4),
        (3, 1),
        (4, 3),
        (4, 2)
    ])

    print(network)
    network.step()
    network.step()
    print(network)
