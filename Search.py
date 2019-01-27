import argparse
import collections
import time

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
def DFS(g, q, adj, pop):
    openedList = []
    for key in adj:
        if(key in pop):
            pass
        else:
            openedList.append(key)
    sortedList = sorted(openedList)
    sortedList.reverse()
    for element in sortedList:
        item = []
        item.append(element)
        item.extend(pop)
        q.extendleft([item])
    return q


#Breadth 1st Search
def BFS(g, q, adj, pop):
    openedList = []
    for key in adj:
        if(key in pop):
            pass
        else:
            openedList.append(key)
    sortedList = sorted(openedList)
    for element in sortedList:
        item = []
        item.append(element)
        item.extend(pop)
        q.extend([item])
    return q

#Depth-Limited Search w/ depth-limit=2
def DLS(g, q, adj, pop):
    if(len(pop)<3):
        openedList = []
        for key in adj:
            if(key in pop):
                pass
            else:
                openedList.append(key)
        sortedList = sorted(openedList)
        sortedList.reverse()
        for element in sortedList:
            item = []
            item.append(element)
            item.extend(pop)
            q.extendleft([item])
    return q

#Iterative Deepening Search (All iterations shown)
def IDS(g, q, adj, pop, i):
    if(len(pop)<i):
        openedList = []
        for key in adj:
            if(key in pop):
                pass
            else:
                openedList.append(key)
        sortedList = sorted(openedList)
        sortedList.reverse()
        for element in sortedList:
            item = []
            item.append(element)
            item.extend(pop)
            q.extendleft([item])
    return q, i

#Specialized Insertion sort according to output specifications
def insertSort(path, q):
    i=0

    if(len(q)==0):
        q.append(path)
    else:
        queueLength = len(q)
        while(i < queueLength):
            if(q[i][1]!=path[1]):
                if(q[i][1]>path[1]):
                    q.insert(i, path)
                    return q
                else:
                    i+=1
            else:
                if(q[i][0][0]!=path[0][0]):
                    if(q[i][0][0]>path[0][0]):
                        q.insert(i, path)
                        return q
                    else:
                        i+=1
                else:
                    if(len(q[i][0])!=len(path[0])):
                        if(len(q[i][0])>len(path[0])):
                            q.insert(i, path)
                            return q
                        else:
                            i+=1
                    else:
                        for j in range(len(path[0])):
                            if(q[i][0][j]>path[0][j]):
                                q.insert(i, path)
                                return q

                        i+=1
        q.append(path)
    return q

#Uniform Cost Search a.k.a Branch-and-Bound
def UCS(g, q, adj, pop):
    openedList = []
    paths = []
    pathcost = pop[1]

    for key in adj:
        if(key in pop[0]):
            pass
        else:
            openedList.append(key)
    #sortedList = sorted(openedList)
    #Need to find new paths with cost then append/insert at correct indexself.
    for node in openedList:
        item = []
        item.append(node)
        item.extend(pop[0])
        #print(item)
        paths.append([item, pathcost + g.getNode(pop[0][0]).getEdgeWeight(node)])

    #Perform insertion sort on queue with the paths
    for path in paths:
        q = insertSort(path, q)

    return q

#Greedy Search a.k.a Best 1st Search
def GS(g, q, adj, pop):
    openedList = []
    paths = []
    pathcost = pop[1]

    for key in adj:
        if(key in pop[0]):
            pass
        else:
            openedList.append(key)

    #Need to find new paths with cost then append/insert at correct indexself.
    for node in openedList:
        item = []
        item.append(node)
        item.extend(pop[0])
        #print(item)
        paths.append([item, g.getNode(node).getNodeWeight()])

    #Perform insertion sort on queue with the paths
    for path in paths:
        q = insertSort(path, q)

    return q

#A*
def ASS(g, q, adj, pop):
    openedList = []
    paths = []

    pathcost = 0
    if(len(pop[0])>1):
        for i in range(len(pop[0])-1):
            pathcost += g.getNode(pop[0][i]).getEdgeWeight(pop[0][i+1])

    for key in adj:
        if(key in pop[0]):
            pass
        else:
            openedList.append(key)

    #Need to find new paths with cost then append/insert at correct indexself.
    for node in openedList:
        item = []
        item.append(node)
        item.extend(pop[0])
        heuristic = (g.getNode(node).getNodeWeight()
                      + g.getNode(pop[0][0]).getEdgeWeight(node)
                      + pathcost)

        place = True
        for i in q:
            if(node==i[0][0]):
                if(heuristic < i[1]):
                    place = True
                else:
                    place = False

        if(place==True):
            paths.append([item, heuristic])



    #Perform insertion sort on queue with the paths
    for path in paths:
        q = insertSort(path, q)
    return q

#Hill-climbinging without backtracking
def HC(g, adj, pop):
    openedList = []
    paths = []
    q = collections.deque([])

    for key in adj:
        if(key in pop[0]):
            pass
        else:
            openedList.append(key)

    #Need to find new paths with cost then append/insert at correct indexself.
    for node in openedList:
        item = []
        item.append(node)
        item.extend(pop[0])
        paths.append([item, g.getNode(node).getNodeWeight()])

    #Perform insertion sort on queue with the paths
    for path in paths:
        q = insertSort(path, q)

    return q

def max_value(inputlist):
    return inputlist.index(max([sublist[-1] for sublist in inputlist]))

def sortMax(q):

    myList = []
    for i in q:
        myList.append(i)
    max = max_value(myList)
    print(max)
    return max(list)

#Beam search with width=2
def BS(g, q, adj, pop):
    openedList = []
    paths = []
    width = 2
    for key in adj:
        if(key in pop[0]):
            pass
        else:
            openedList.append(key)

    sortedList = sorted(openedList)

    for node in sortedList:
        item = []
        item.append(node)
        item.extend(pop[0])
        paths.append([item, g.getNode(node[0]).getNodeWeight()])

    for path in paths:
        q.extend([path])

    #Check the width condition
    if(len(q[0][0])!=len(pop[0])):
       while(len(q)>width):
           n = 0
           i = 0
           while(i<len(q)):
               if(q[n][1]>=q[i][1]):
                   i+=1
               else:
                   n+=1
                   i = 0
           q.remove(q[n])
           #vals = []
           #for i in range(len(q)):
            #   vals.append(q[i][1])
           #maximum = sortMax(q)
           #q.remove(maximum)
           #for i in range(len(q):
        #       if(q[n][1]>=q[i][1]):

         #  for i in range(len(q)):
        #       for j in range(len(q)-1):
        #           if((j+1)==i)
        #           if(q[i][1]>=q[j+1][1])


    time.sleep(1)
    return q

def printRow(expanded, queue):
    print("{:>15} {:>10}".format(expanded, queue))

def printExpanded(expanded, queue):
    print("{:>11} {:>14}".format(expanded, queue))

#General Search Procedure to be called
#Input: Graph txt File
def General_Search(graph, searchMethod):
    print("*" + searchMethod + ":")
    printRow('Expanded', 'Queue')
    i=1
    #Initialize the Queue
    if(searchMethod == 'UCS'):
        node = [['S'], 0]
        q=collections.deque([node])
        printExpanded('S', '[0<S>]')
    elif(searchMethod == 'GS'):
        node = [['S'], graph.getNode('S').getNodeWeight()]
        q=collections.deque([node])
        printExpanded('S', "[{val}<S>]".format(val = node[1]))
    elif(searchMethod == 'ASS'):
        node = [['S'], graph.getNode('S').getNodeWeight()]
        q=collections.deque([node])
        printExpanded('S', "[{val}<S>]".format(val = node[1]))
    elif(searchMethod == 'HC'):
        node = [['S'], graph.getNode('S').getNodeWeight()]
        q=collections.deque([node])
        printExpanded('S', "[{val}<S>]".format(val = node[1]))
    elif(searchMethod == 'BS'):
        node = [['S'], graph.getNode('S').getNodeWeight()]
        q=collections.deque([node])
        printExpanded('S', "[{val}<S>]".format(val = node[1]))
    elif(searchMethod == 'IDS'):
        node = ['S']
        q=collections.deque([node])
        print("{} {:>7} {:>14}".format('L=0','S','[<S>]'))
    else:
        node = ['S']
        q=collections.deque([node])
        printExpanded('S', '[<S>]')


    while True:
        #If Queue is empty, Return No solution
        if(len(q)==0):
            if(searchMethod=='IDS'):
                node = ['S']
                q=collections.deque([node])
                print("{} {:>7} {:>14}".format('L=0','S','[<S>]'))
                i+=1
            else:
                print('Path not found :(\n')
                break
        #printSearch(e, q)
        pop = q.popleft() #Pop From Queue
        print(pop)
        #If Node is goal, return solution
        if(pop[0][0]=='G'):
            print('Goal reached!\n')
            return pop
            break

        #Expand from the pop top node
        if(searchMethod == ('DFS' or 'BFS' or 'IDS')):
            adj = g.getNode(pop[0]).getAdjacent()
        else:
            adj = g.getNode(pop[0][0]).getAdjacent()
        #print(adj)

        #Update queue according to the search method
        if(searchMethod == 'DFS'):
            q = DFS(g, q, adj, pop)

        if(searchMethod == 'BFS'):
            q = BFS(g, q, adj, pop)

        if(searchMethod == 'DLS'):
            q = DLS(g, q, adj, pop)

        if(searchMethod == 'IDS'):
            q,i = IDS(g, q, adj, pop, i)

        if(searchMethod == 'UCS'):
            q = UCS(g, q, adj, pop)

        if(searchMethod == 'GS'):
            q = GS(g, q, adj, pop)

        if(searchMethod == 'ASS'):
            q = ASS(g, q, adj, pop)

        if(searchMethod == 'HC'):
            q = HC(g, adj, pop)

        if(searchMethod == 'BS'):
            q = BS(g, q, adj, pop)

        print(q)


if __name__== "__main__":
    parser = argparse.ArgumentParser(description='Perform Graph Searches')
    parser.add_argument('graphFile')
    #parser.add_argument('outputFile')
    args = parser.parse_args()

    g = Graph()

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
    searchMethods = ['DFS', 'BFS',
                     'DLS', 'IDS',
                     'UCS', 'GS',
                     'ASS', 'HC', 'BS']

    for searchMethod in searchMethods:
        General_Search(g, searchMethod)
