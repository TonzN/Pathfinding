import ui
import random
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

grid = ui.grid(window.Size, 20, False)
grid.border = True
grid.generate(screen)

#grid.colorRegion([[10, 20], [20,30]], (255,0,0))

print("--------Grid Data---------")
print("Grid size", grid._pos.shape)

counter = 0
ycounter = 0

ui.KeyBindFunctions[ui.pygame.K_b] = buildObst

window.Target_fps = 120

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


graphRects = {}


print(graph.get(graph.rootNode, True))


def sortString(str):
    return ''.join(sorted(str))

#FOR UNDIRECTED GRAPHS!!
def displayGraph():
    #For drawing nodes 
    listGraph = graph.get(graph.rootNode)
    for i in listGraph:
        xPos, yPos = math.floor(listGraph[i].Pos[0]/20), math.floor(listGraph[i].Pos[1]/20)
        grid.colorBlock((xPos, yPos), (50,50,200))

    connections = {}
    for i in listGraph:
        for z in listGraph[i].Adjacent:
            key = sortString(str(listGraph[i].Value) + str(listGraph[i].Adjacent[z][0].Value))
            if not key in connections:
                connections[key] = (listGraph[i].Pos, listGraph[i].Adjacent[z][0].Pos)
    
    for i in connections:
        start = (connections[i][0][0]+10,connections[i][0][1]+10)
        end = (connections[i][1][0]+10,connections[i][1][1]+10)
        ui.Line(screen, (150,150,150), start, end, 4)

   
def visualzeDFS(graph, node):
    found, History = graph.dfs(node, True)
    region = []
     
    for i in History:
        xPos, yPos = math.floor(History[i].Pos[0]/20), math.floor(History[i].Pos[1]/20)
        
        if found.Pos == History[i].Pos:
            grid.colorBlock((xPos, yPos), (100,200,100))
        else:
            grid.colorBlock((xPos, yPos), (200,100,100))

        region.append((xPos, yPos))
        
        
        counter = 0
        while counter <= 10:
            counter += 1
            window.NextFrame()
    
    grid.regionColorHistory["VisualizeDFS"] = region
    grid.refreshRegion("VisualizeDFS",  (50,50,200))
    

    
   
    
displayGraph()

while True:
    window.NextFrame()
    visualzeDFS(graph, "G")
    
   
    
    grid.refreshColours()
    
