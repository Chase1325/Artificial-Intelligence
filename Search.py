import argparse
from queue import PriorityQueue

class Node:
    def __init__(self, node, weight=0):
        self.node = node
        self.adjacent = {}
        self.weight = weight

    #Add an adjacent node and their weight
    def addAdjacent(self, adj, weight=0):
        self.adjacent[adj] = weight

    #Get the adjacent nodes
    def getAdjacent(self):
        return self.adjacent.keys()

    #Get the node name
    def getNode(self):
        return self.node

    def getNodeWeight(self):
        return self.weight

    #Get the weight of the edge
    def getEdgeWeight(self, adj):
        return self.adjacent[adj]

class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}

    def addNode(self, node, weight):
        self.nodes[node] = Node(node, weight)

    def addEdge(self, node1, node2, weight):
        if node1 in self.nodes:
            if node2 not in self.nodes[node1].getAdjacent():
                self.nodes[node1].addAdjacent(node2, weight)
        if node2 in self.nodes:
            if node1 not in self.nodes[node2].getAdjacent():
                self.nodes[node2].addAdjacent(node1, weight)

    def getNode(self, node):
        if node in self.nodes:
            return self.nodes[node]
        else:
            return None

    def getAllNodes(self):
        return self.nodes.keys()

    def getAllEdges(self):
        return self.edges


#Depth 1st Search
def depthFirst():
    pass

#Breadth 1st Search
def breadthFirst():
    pass

#Depth-Limited Search w/ depth-limit=2
def depthLimited():
    pass

#Iterative Deepening Search (All iterations shown)
def iterativeDeep():
    pass

#Uniform Cost Search a.k.a Branch-and-Bound
def uniformCost():
    pass

#Greedy Search a.k.a Best 1st Search
def greedy():
    pass

#A*
def aStar():
    pass

#Hill-climbinging without backtracking
def hillClimbNoBacktrack():
    pass

#Beam search with width=2
def beam():
    pass

def searchHandle(Queue, searchMethod):
    searchMethodSwitch = {
        'Depth 1st Search': 0,
        'Breadth 1st Search': 1,
        'Depth-limited Search': 2,
        'Iterative Deepening Search': 3,
        'Uniform Cost Search': 4,
        'Greedy Search': 5,
        'A*': 6,
        'Hill-climbing': 7,
        'Beam Search': 8,
    }

    return searchMethodSwitch.get(searchMethod, 'Method non existent')

def printRow(expanded, queue):
    print("{:>15} {:>10}".format(expanded, queue))

#General Search Procedure to be called
#Input: Graph txt File
def General_Search(graph, searchMethod):
    print("*" + searchMethod + ":\n")
    printRow('Expanded', 'Queue')
    #q=[]
    #if q.isEmpty():
    #    pass
    #searchHandle(q, searchMethod)


if __name__== "__main__":
    parser = argparse.ArgumentParser(description='Perform Graph Searches')
    parser.add_argument('graphFile')
    parser.add_argument('outputFile')
    args = parser.parse_args()

    g = Graph()

    #outputFile = open(args.outputFile, 'w')
    #outputFile.write("Test")

    nodeInfo = []
    edgeInfo = []

    with open(args.graphFile, mode='r') as file:

        lines = file.readlines()
        node=False

        for line in lines:
            if '#####\n' in line:
                node=True
                continue
            if(node==False):
                line = line.rstrip('n').split()
                edgeInfo.append([line[0],line[1],float(line[2])])
                #g.addEdge(line[0],line[1], float(line[2]))
            else:
                line = line.rstrip('n').split()
                nodeInfo.append([line[0], float(line[1])])
                #g.addNode(line[0], float(line[1]))
    nodeInfo.append(['G', 0.0]) #Goalstate

    #Populate our graph with info
    for node in nodeInfo:
        g.addNode(node[0],node[1])
    for edge in edgeInfo:
        g.addEdge(edge[0],edge[1],edge[2])

    #print(g.getNode('A').getAdjacent())
    searchMethods = ['Depth 1st Search', 'Breadth 1st Search',
                     'Depth-limited Search', 'Iterative Deepening Search',
                     'Uniform Cost Search', 'Greedy Search', 'A*',
                     'Hill-climbing', 'Beam Search']
    for searchMethod in searchMethods:
        General_Search(g, searchMethod)
