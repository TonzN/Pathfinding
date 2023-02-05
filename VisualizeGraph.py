import ui
import random
import string
import math
import datastructures as ds

window = ui.NewWindow("PathFinding", )
window.BGColor = (0,0,0)
screen = window.screen
cellSize = 40

def buildObst():
    mPos = window.mousepos
    xPos, yPos = math.floor(mPos[0]/cellSize), math.floor(mPos[1]/cellSize)
    grid.colorBlock((xPos, yPos), (150,150,150))
    #print(xPos, yPos)

def sortString(str):
    return ''.join(sorted(str))

#FOR UNDIRECTED GRAPHS!!
def displayGraph():
    #For drawing nodes 
    listGraph = graph.get(graph.rootNode)
    for i in listGraph: #displays all the connected nodes of the graphS
        xPos, yPos = math.floor(listGraph[i].Pos[0]/cellSize), math.floor(listGraph[i].Pos[1]/cellSize) #turns positions into grid location x, y 
        # /size of cells
        grid.colorBlock((xPos, yPos), (50,50,200))
    
    for i in graph.UnConnected:
        xPos, yPos = math.floor(graph.UnConnected[i].Pos[0]/cellSize), math.floor(graph.UnConnected[i].Pos[1]/cellSize)
        grid.colorBlock((xPos, yPos), (50,50,200))

    connections = {}

    for i in graph.UnConnected:
        listGraph[i] = graph.UnConnected[i]
    
        
    for i in listGraph: #adds the edges to connectionsS
        for z in listGraph[i].Adjacent:
            key = sortString(str(listGraph[i].Value) + str(listGraph[i].Adjacent[z][0].Value)) #sorts the keynames alphabethically so duplicate connections dont happenS
            if not key in connections:
                connections[key] = (listGraph[i].Pos, listGraph[i].Adjacent[z][0].Pos)
    
    for i in connections: #to draw the edges"
        start = (connections[i][0][0]+cellSize/2,connections[i][0][1]+cellSize/2)
        end = (connections[i][1][0]+cellSize/2,connections[i][1][1]+cellSize/2)
        ui.Line(screen, (150,150,150), start, end, 4)
  
def runFor(itr): #run just nextFrames for itr
    counter = 0
    while counter <= itr: 
        counter += 1
        window.NextFrame()

def visualzeDFS(graph, node):
    found, History = graph.dfs(node, False, True)
    region = []
     
    if History == False:
        return

    for i in History:
        xPos, yPos = math.floor(History[i].Pos[0]/cellSize), math.floor(History[i].Pos[1]/cellSize)
        
        if found.Pos == History[i].Pos:
            grid.colorBlock((xPos, yPos), (100,200,100)) #Color end green
            region.append((xPos, yPos))
            runFor(30)
            break

        else:
            grid.colorBlock((xPos, yPos), (200,100,100)) #rest red
            region.append((xPos, yPos))

        runFor(10)
    
    grid.regionColorHistory["VisualizeDFS"] = region
    grid.refreshRegion("VisualizeDFS",  (50,50,200))

def visualizeDjistras(graph, path, target):
    region = []
    nodes = graph.get(graph.rootNode)
    print("PATH", path)

    for i in path:
        xPos, yPos = math.floor(nodes[i].Pos[0]/cellSize), math.floor(nodes[i].Pos[1]/cellSize)

        if i == target:
            grid.colorBlock((xPos, yPos), (100,200,100))
            region.append((xPos, yPos))
            runFor(30)
            break

        else:
            grid.colorBlock((xPos, yPos), (200,100,100)) #rest red
            region.append((xPos, yPos))

        runFor(10)
    
    grid.regionColorHistory["VisualizeDFS"] = region
    grid.refreshRegion("VisualizeDFS",  (50,50,200))


def setDFS():
    node = graph.dfs(False, False, False, (math.floor(window.mousepos[0]/cellSize)*cellSize, math.floor(window.mousepos[1]/cellSize)*cellSize))
    if node:
        graph.searchForNode = node.Value
    else:
        graph.searchForNode = False

def printGraph():
    graph.get(graph.rootNode, True)

def setDjikstras():
    node = graph.dfs(False, False, False, (math.floor(window.mousepos[0]/cellSize)*cellSize, math.floor(window.mousepos[1]/cellSize)*cellSize))
    if node:
        graph.RunDjikstra = node.Value
    else:
        graph.RunDjikstra = False

# KEYBIND SETUP
ui.KeyBindFunctions[ui.pygame.K_b] = buildObst #To make buildObst a keybind function to b
ui.KeyBindFunctions[ui.pygame.K_f] = setDFS
ui.KeyBindFunctions[ui.pygame.K_g] = printGraph
ui.KeyBindFunctions[ui.pygame.K_p] = setDjikstras


#-----#

window.Target_fps = 120

SelectedNode1 = None

grid = ui.grid(window.Size, cellSize, False)
grid.border = True
grid.generate(screen)

#grid.colorRegion([[10, 20], [20,30]], (255,0,0))

print("\n--------Grid Data---------")
print("Grid size", grid._pos.shape)


# GRAPH SETUP 
g_Node = ds.g_Node
graph = ds.Graph()
graph.rootNode.Pos = (360,320)


print("\n--------Key binds---------")
print("Right Click: Make new node over where your mouse hover\n")
print("Left Click to select a node to connnect --> right click to choose which to connect too || Left click again to cancel\n")
print("F to visualize DFS, target is over mouse posititon || F on a empty square to cancel\n")
print("G to print out the graph \n")
print("P to find shortest path to node || hover over node \n")
print("B to just color a square grey || Not important tbh\n")



while True: 
    window.NextFrame()

    pos = (math.floor(window.mousepos[0]/cellSize)*cellSize, math.floor(window.mousepos[1]/cellSize)*cellSize)
    
    if window.rightclick():
        if not SelectedNode1:
            x = random.choice(string.ascii_letters)
            x2 = random.choice(string.ascii_letters)
            x3 = random.choice(string.ascii_letters)
            graph.AddUnConnected(g_Node(x+x2+x3, pos))
            displayGraph()
        else:
            node = graph.dfs(False, False, False, pos)
            if node:
                print("CONNECTING")
                graph.Add(SelectedNode1, node)
                displayGraph()
            elif graph.findUnconnected(False, pos):
                print("CONNECTING")
                graph.Add(SelectedNode1, graph.findUnconnected(False, pos))
                displayGraph()
     
    if window.leftclick():
        if not SelectedNode1:
            node = graph.dfs(False, False, False, pos)
            if node:
                SelectedNode1 = node
            elif graph.findUnconnected(False, pos):
                SelectedNode1 = graph.findUnconnected(False, pos)
            
            if SelectedNode1:
                print("SELECTED NODE -->", SelectedNode1.Value, "\n")
                
        else:
            SelectedNode1 = None
        
    
    if graph.searchForNode:
        visualzeDFS(graph, graph.searchForNode)
        graph.searchForNode = False

    if graph.RunDjikstra:
        path = graph.djikstras(graph.rootNode, graph.RunDjikstra, True)
        visualizeDjistras(graph, path, graph.RunDjikstra)
        graph.RunDjikstra = False
    
