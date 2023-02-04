import ui
import random
import math
import datastructures as ds

window = ui.NewWindow("PathFinding", )
window.BGColor = (0,0,0)
screen = window.screen


def buildObst():
    mPos = window.mousepos
    xPos, yPos = math.floor(mPos[0]/10), math.floor(mPos[1]/10)
    grid.colorBlock((xPos, yPos), (150,150,150))
    print(xPos, yPos)

grid = ui.grid(window.Size, 10, False)
grid.border = True
grid.generate(screen)

print("--------Grid Data---------")
print("Grid size", grid._pos.shape)

counter = 0
ycounter = 0

ui.KeyBindFunctions[ui.pygame.K_b] = buildObst

window.Target_fps = 120

g_Node = ds.g_Node
graph = ds.Graph()
graph.rootNode.Pos = (350,280)
graph.Add(graph.rootNode, g_Node("A", (370, 280)))
graph.Add(graph.rootNode, g_Node("B", (350, 280)))
graph.Add(graph.dfs("B"), g_Node("C"))
graph.Add(graph.rootNode, g_Node("D"))
graph.Add(graph.dfs("C"), graph.rootNode)
graph.Add(graph.dfs("B"), g_Node("E"))
graph.Add(graph.dfs("E"), graph.dfs("C") )
graph.Add(graph.dfs("E"), g_Node("u"))
#graph.show(graph.rootNode)



def displayGraph():
    pass

while True:
    window.NextFrame()
    grid.refreshColours()
    