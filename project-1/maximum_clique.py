# ----------------------------------------------
# Introduction to Artificial Intelligence
# Fall 2014
# Author: Vishwanath Sangale
# ----------------------------------------------

import re


# class graph
class Graph:
    def __init__(self, graph_file):
        self.numberOfNodes = 0
        self.givenInputFile = graph_file
        self.alreadyPresentNode = list()
        # Open the given file
        self.create_graph(graph_file)
        self.adjacencyMatrix = [[0 for _ in range(self.numberOfNodes)] for __ in range(self.numberOfNodes)]

    def create_graph(self, graph_file):
        f = open(graph_file, 'r')
        # Parse each line of the file
        for line in f:
            # Check if line contains any comment and remove them
            line = re.sub('//.*?\n|/\*.*?\*/', '', line, re.S)
            if ';' in line:
                line = re.sub('	|;', '', line, re.S)
                line = re.sub('\n| ', '', line, re.S)
                first_node, delimiter, second_node = line.partition('--')
                if self.numberOfNodes == 0:
                    self.numberOfNodes += 1
                    self.alreadyPresentNode.append(first_node)
                for x in range(0, self.numberOfNodes):
                    if first_node == '':
                        break
                    if first_node != self.alreadyPresentNode[x]:
                        if x == self.numberOfNodes - 1:
                            self.numberOfNodes += 1
                            self.alreadyPresentNode.append(first_node)
                        continue
                    else:
                        break
                for x in range(0, self.numberOfNodes):
                    if second_node == '':
                        break
                    if second_node != self.alreadyPresentNode[x]:
                        if x == self.numberOfNodes - 1:
                            self.numberOfNodes += 1
                            self.alreadyPresentNode.append(second_node)
                        continue
                    else:
                        break
        f.seek(0)
        f.close()

    def create_adjacency_matrix(self):
        f = open(self.givenInputFile, 'r')
        for line in f:
            line = re.sub('//.*?\n|/\*.*?\*/', '', line, re.S)
            if ';' in line:
                line = re.sub('	|;', '', line, re.S)
                line = re.sub('\n| ', '', line, re.S)
                for i in range(0, self.numberOfNodes):
                    for j in range(0, self.numberOfNodes):
                        if self.alreadyPresentNode[i] + "--" + self.alreadyPresentNode[j] in line:
                            self.adjacencyMatrix[i][j] = 1
                            self.adjacencyMatrix[j][i] = 1
        f.close()


# Function to get all subsets of given vertices.
def get_all_subsets_of_all_vertices(nodes):
    if len(nodes) == 0:
        return [[]]
    else:
        subsetsWithoutEmpty = get_all_subsets_of_all_vertices(nodes[1:])
        subsetsWithEmpty = []
        for i in subsetsWithoutEmpty:
            subsetsWithEmpty.append(i + [nodes[0]])
        allSubsets = subsetsWithoutEmpty + subsetsWithEmpty
        return allSubsets


# Function to check if given subset is connected or not.
def is_this_subset_connected(Graph, subset):
    for i in subset:
        for j in subset:
            if not i == j:
                if not 1 == Graph.adjacencyMatrix[Graph.alreadyPresentNode.index(i)][Graph.alreadyPresentNode.index(j)]:
                    return False
    return True


# Function to get all connected subsets from all subsets of vertices.
def get_all_connected_subsets(Graph, allSubsets):
    connectedSubsets = []
    for subset in allSubsets:
        if is_this_subset_connected(Graph, subset):
            connectedSubsets.append(subset)
    return connectedSubsets


# Function to calculate the maximum size from the given connected subsets.
def calculate_maximum_size_of_connected_subset(connectedSubsets):
    maxSizeOfSubSet = 0
    for subset in connectedSubsets:
        if len(subset) > maxSizeOfSubSet:
            maxSizeOfSubSet = len(subset)
    return maxSizeOfSubSet


def maximum_clique(Graph):
    Graph.create_adjacency_matrix()
    allSubsets = get_all_subsets_of_all_vertices(Graph.alreadyPresentNode)
    connectedSubsets = get_all_connected_subsets(Graph, allSubsets)
    print "Size of the maximum clique in a given graph is"
    return calculate_maximum_size_of_connected_subset(connectedSubsets)
