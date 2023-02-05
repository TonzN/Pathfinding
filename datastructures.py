import ui
import math
import heapq

class PriorityQueue:
    def __init__(self):
        pass

class g_Node:
    def __init__(self, val = 0, pos = (0,0)):
        self.Adjacent = { #Key->[node, weight]
        }
        self.Value = val 
        self.Pos = pos


class Graph:
    def __init__(self):
        self.rootNode = g_Node() 
        self.UnConnected = {}   
        self.searchForNode = False #Only for visualization purposes
        self.RunDjikstra = False # --^^--
    
    def AddUnConnected(self, node): #unconnected nodes --> no edges 
        self.UnConnected[node.Value] = node
    
    def findUnconnected(self, node = False, position = False, value = False):
        for i in self.UnConnected: 
            if self.UnConnected[i] == node:
                return self.UnConnected[i]
            elif self.UnConnected[i].Pos == position:
                return self.UnConnected[i]
            elif self.UnConnected[i].Value == value:
                return self.UnConnected[i]
       # print("DID NOT FIND")
        return False

    def Add(self, node, newNode): #Undirected --> makes connections not nodes!
        if node.Value in newNode.Adjacent:
            print("ALREADY CONNECTED")
        else:
            sumA = node.Pos[0] + node.Pos[1]
            sumB = newNode.Pos[0] + newNode.Pos[1]
            distance = abs(sumB-sumA)
            node.Adjacent[newNode.Value] = [newNode, distance] # [node, edgedistance] 
            newNode.Adjacent[node.Value] = [node, distance] 
            print("CONNECTED", node.Value, newNode.Value)
    
    def traverse(self):
        pass

    def Remove(self):
        pass

    def get(self, node, Show = False): #print or get a dictionary of all the nodes
        stack = [node]
        visited = {} 
        visited[node.Value] = node
    
        while stack:
            current_node = stack.pop()
            if Show:
                print(current_node.Value, current_node.Adjacent, "\n")
            visited[current_node.Value] = current_node
            if current_node.Adjacent is not None and current_node.Adjacent:
                for i in current_node.Adjacent:
                    if current_node.Adjacent[i][0].Value not in visited:
                        stack.append(current_node.Adjacent[i][0])
                        visited[current_node.Adjacent[i][0].Value] = current_node.Adjacent[i][0]
        return visited

    def dfs(self, node, start = False, history = False, PosOfNode = False):
        stack = [start or self.rootNode]
        visited = {}
        visited[stack[0].Value] = stack[0]
        while stack:
            current = stack.pop()
            if PosOfNode:
                if current.Pos == PosOfNode: #find node by position
                    return current
            else:
                if current.Value == node:
                    if history == True:
                        return current, visited #if you need the history of nodes visited
                    else:
                        return current 

            if current.Adjacent is not None and current.Adjacent:
                for i in current.Adjacent:
                    adjacent_node = current.Adjacent[i][0]
                    if adjacent_node.Value not in visited:
                        stack.append(adjacent_node)
                        visited[adjacent_node.Value] = adjacent_node
     
     #   print("Did not find node!")
        return False

    def djikstras(self, Start, Target, Visualize = False):
        nodes = self.get(Start)
        distances = {node: float("infinity") for node in nodes}
        distances[Start.Value] = 0
        previous = {node: None for node in nodes}

        queue = [(0, Start.Value)]

        while queue:
            current_distance, current_Node = heapq.heappop(queue) #gets highest priority node --> shortest distance

            if current_Node == Target:
                break

            if current_distance > distances[current_Node]:
                continue
            
            for neighbor, adjacent in nodes[current_Node].Adjacent.items(): #gets the neighbor and adjacent variables
                distance = current_distance + adjacent[1] #adds distance so you get the total distance from start to the adjacent 

                if distance < distances[neighbor]: #if the distance is shorter it adds it to the priority queue and previous which is used to make the path
                    distances[neighbor] = distance
                    previous[neighbor] = current_Node
                    heapq.heappush(queue, (distance, neighbor))
            
            
        path = []
        current = Target
        while current is not None:
            path.append(current)
            current = previous[current]

        path.reverse()
        return path


