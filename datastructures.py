import ui


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
    
    def Add(self, node, newNode): #Undirected --> makes connections not nodes!
        sumA = node.Pos[0] + node.Pos[1]
        sumB = newNode.Pos[0] + newNode.Pos[1]
        distance = sumB-sumA
        node.Adjacent[newNode.Value] = [newNode, distance] # [node, edgedistance] 
        newNode.Adjacent[node.Value] = [node, distance]

    def traverse(self):
        pass

    def Remove(self):
        pass

    def get(self, node, Show = False):
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


    def dfs(self, node, history = False):
        stack = [self.rootNode]
        visited = {}
        visited[self.rootNode.Value] = self.rootNode
        while stack:
            current = stack.pop()
            if current.Value == node:
                if history == True:
                    return current, visited
                else:
                    return current
            if current.Adjacent is not None and current.Adjacent:
                for i in current.Adjacent:
                    adjacent_node = current.Adjacent[i][0]
                    if adjacent_node.Value not in visited:
                        stack.append(adjacent_node)
                        visited[adjacent_node.Value] = adjacent_node

        print("Did not find node!")

    def djikstras(Start, End):
        pass        


