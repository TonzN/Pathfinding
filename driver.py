import ui
import random
import string
import math
import datastructures as ds

window = ui.NewWindow("PathFinding", )
window.BGColor = (0,0,0)
screen = window.screen


def buildObst():
    mPos = window.mousepos
    xPos, yPos = math.floor(mPos[0]/20), math.floor(mPos[1]/20)
    grid.colorBlock((xPos, yPos), (150,150,150))
    #print(xPos, yPos)

def sortString(str):
    return ''.join(sorted(str))

#FOR UNDIRECTED GRAPHS!!
def displayGraph():
    #For drawing nodes 
    listGraph = graph.get(graph.rootNode)
    for i in listGraph: #displays all the connected nodes of the graphS
        xPos, yPos = math.floor(listGraph[i].Pos[0]/20), math.floor(listGraph[i].Pos[1]/20) #turns positions into grid location x, y 
        # /size of cells
        grid.colorBlock((xPos, yPos), (50,50,200))
    
    for i in graph.UnConnected:
        xPos, yPos = math.floor(graph.UnConnected[i].Pos[0]/20), math.floor(graph.UnConnected[i].Pos[1]/20)
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
        start = (connections[i][0][0]+10,connections[i][0][1]+10)
        end = (connections[i][1][0]+10,connections[i][1][1]+10)
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
        xPos, yPos = math.floor(History[i].Pos[0]/20), math.floor(History[i].Pos[1]/20)
        
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


def setDFS():
    node = graph.dfs(False, False, False, (math.floor(window.mousepos[0]/20)*20, math.floor(window.mousepos[1]/20)*20))
    if node:
        graph.searchForNode = node.Value
    else:
        graph.searchForNode = False
    

# KEYBIND SETUP
ui.KeyBindFunctions[ui.pygame.K_b] = buildObst #To make buildObst a keybind function to b
ui.KeyBindFunctions[ui.pygame.K_f] = setDFS

#-----#

window.Target_fps = 120

SelectedNode1 = None

grid = ui.grid(window.Size, 20, False)
grid.border = True
grid.generate(screen)

#grid.colorRegion([[10, 20], [20,30]], (255,0,0))

print("--------Grid Data---------")
print("Grid size", grid._pos.shape)



# GRAPH SETUP 
g_Node = ds.g_Node
graph = ds.Graph()
graph.rootNode.Pos = (360,320)
graph.Add(graph.rootNode, g_Node("A", (340, 280)))
graph.Add(graph.rootNode, g_Node("B", (380, 280)))
graph.Add(graph.dfs("B"), g_Node("C", (380, 220)))
graph.Add(graph.dfs("B"), g_Node("D", (420, 220)))
graph.Add(graph.dfs("B"), g_Node("E", (400, 320)))
graph.Add(graph.dfs("C"), g_Node("F", (460, 280)))
graph.Add(graph.dfs("F"), g_Node("G", (520, 360)))


displayGraph()

while True:
    window.NextFrame()

    pos = (math.floor(window.mousepos[0]/20)*20, math.floor(window.mousepos[1]/20)*20)
    
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
                print(SelectedNode1.Value)
                
        else:
            SelectedNode1 = None
        
    
    if graph.searchForNode:
        visualzeDFS(graph, graph.searchForNode)
    
