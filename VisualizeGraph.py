import ui
import random
import string
import math
import datastructures as ds

window = ui.NewWindow("PathFinding", )
window.BGColor = (0,0,0)
screen = window.screen
cellSize = 10
screen_size = window.Size
frameskip = 60
layerskips = 3
window.Target_fps = 120

NODE_COLOR = (50,50,200)
ROOT_COLOR = (200,50,50)
HOVER_COLOR = (50,200,100)
PATH_COLOR = (200,100,100)
TARGET_COLOR = (100,200,100)

def buildObst():
    mPos = window.mousepos
    xPos, yPos = math.floor(mPos[0]/cellSize), math.floor(mPos[1]/cellSize)
    grid.colorBlock((xPos, yPos), (150,150,150))

def sortString(str):
    return ''.join(sorted(str))

def getMousePos():
    return (math.floor(window.mousepos[0]/cellSize)*cellSize, math.floor(window.mousepos[1]/cellSize)*cellSize)

def getMouseNode():
    return node_by_pos.get(getMousePos())

#FOR UNDIRECTED GRAPHS!!
def displayGraph():
    for pos in node_by_pos:
        xPos, yPos = pos[0]//cellSize, pos[1]//cellSize
        grid.colorBlock((xPos, yPos), NODE_COLOR)

    #root node always red
    xPos, yPos = graph.rootNode.Pos[0]//cellSize, graph.rootNode.Pos[1]//cellSize
    grid.colorBlock((xPos, yPos), ROOT_COLOR)

def runFor(itr): #run just nextFrames for itr
    counter = 0
    while counter <= itr:
        counter += 1
        window.NextFrame()

def visualzeDFS(graph, node):
    found, History = graph.dfs(node, False, True)
    region = []
    cntr = 0

    if History == False:
        return

    cntr2 = 0
    for i in History:
        cntr2 += 1
        xPos, yPos = math.floor(History[i].Pos[0]/cellSize), math.floor(History[i].Pos[1]/cellSize)

        if found.Pos == History[i].Pos:
            grid.colorBlock((xPos, yPos), TARGET_COLOR)
            region.append((xPos, yPos))
            cntr += 1
            if cntr >= frameskip:
                runFor(1)
                cntr = 0
            break
        else:
            grid.colorBlock((xPos, yPos), PATH_COLOR)
            region.append((xPos, yPos))

        if cntr2 >= layerskips:
            cntr2 = 0
            runFor(1)

    grid.regionColorHistory["VisualizeDFS"] = region
    grid.refreshRegion("VisualizeDFS", NODE_COLOR)
    displayGraph()

def visualizeDjistras(graph, path, target):
    region = []
    nodes = graph.get(graph.rootNode)
    print("PATH", path)
    cntr = 0
    cntr2 = 0

    for i in path:
        cntr2 += 1
        if i not in nodes:
            continue

        xPos, yPos = math.floor(nodes[i].Pos[0]/cellSize), math.floor(nodes[i].Pos[1]/cellSize)

        if i == target:
            grid.colorBlock((xPos, yPos), TARGET_COLOR)
            region.append((xPos, yPos))
            cntr += 1
            if cntr >= frameskip:
                runFor(1)
                cntr = 0    
            break
        else:
            grid.colorBlock((xPos, yPos), PATH_COLOR)
            region.append((xPos, yPos))

        if cntr2 >= layerskips:
            cntr2 = 0
            runFor(1)

    grid.regionColorHistory["VisualizeDjikstra"] = region
    grid.refreshRegion("VisualizeDjikstra", NODE_COLOR)
    displayGraph()

def setDFS():
    node = getMouseNode()

    if node:
        graph.searchForNode = node.Value
    else:
        graph.searchForNode = False

def printGraph():
    graph.get(graph.rootNode, True)

def setDjikstras():
    node = getMouseNode()

    if node:
        graph.RunDjikstra = node.Value
    else:
        graph.RunDjikstra = False

def full_connect_graph():
    global node_by_pos

    cols = window.Size[0] // cellSize
    rows = window.Size[1] // cellSize
    node_by_pos = {}

    #create nodes with around 70% probability
    for y in range(rows):
        for x in range(cols):
            if random.randint(0,100) < 30:
                continue

            pos = (x*cellSize, y*cellSize)
            name = f"{x}_{y}" #unique node value based on position

            node = g_Node(name, pos)
            graph.AddUnConnected(node)
            node_by_pos[pos] = node

    if not node_by_pos:
        return

    #pick random root node
    graph.rootNode = random.choice(list(node_by_pos.values()))

    #connect nodes only to nodes directly right/below
    #assuming Graph.Add makes the connection undirected
    for pos, node in node_by_pos.items():
        x = pos[0] // cellSize
        y = pos[1] // cellSize

        pos_right = ((x+1)*cellSize, y*cellSize)
        pos_below = (x*cellSize, (y+1)*cellSize)

        right_node = node_by_pos.get(pos_right)
        below_node = node_by_pos.get(pos_below)

        if right_node:
            graph.Add(node, right_node)

        if below_node:
            graph.Add(node, below_node)

def updateHover():
    global previous_hover

    pos = getMousePos()

    if pos == previous_hover:
        return

    #reset previous hovered node
    if previous_hover:
        node = node_by_pos.get(previous_hover)

        if node:
            xPos, yPos = previous_hover[0]//cellSize, previous_hover[1]//cellSize

            if node == graph.rootNode:
                grid.colorBlock((xPos, yPos), ROOT_COLOR)
            else:
                grid.colorBlock((xPos, yPos), NODE_COLOR)

    #color current hovered node green
    node = node_by_pos.get(pos)

    if node:
        xPos, yPos = pos[0]//cellSize, pos[1]//cellSize

        if node == graph.rootNode:
            grid.colorBlock((xPos, yPos), ROOT_COLOR)
        else:
            grid.colorBlock((xPos, yPos), HOVER_COLOR)

    previous_hover = pos


# KEYBIND SETUP
ui.KeyBindFunctions[ui.pygame.K_b] = buildObst
ui.KeyBindFunctions[ui.pygame.K_f] = setDFS
ui.KeyBindFunctions[ui.pygame.K_g] = printGraph
ui.KeyBindFunctions[ui.pygame.K_p] = setDjikstras

#-----#

window.Target_fps = 120

SelectedNode1 = None
previous_hover = None

grid = ui.grid(window.Size, cellSize, False)
grid.border = False
grid.EnableNode = True
grid.generate(screen)

print("\n--------Grid Data---------")
print("Grid size", grid._pos.shape)

# GRAPH SETUP
g_Node = ds.g_Node
graph = ds.Graph()

full_connect_graph()
displayGraph()

print("\n--------Key binds---------")
print("Right Click: Make new node over where your mouse hover\n")
print("Left Click to select a node to connnect --> right click to choose which to connect too || Left click again to cancel\n")
print("F to visualize DFS, target is over mouse posititon || F on a empty square to cancel\n")
print("G to print out the graph \n")
print("P to find shortest path to node || hover over node \n")
print("B to just color a square grey || Not important tbh\n")

while True:
    window.NextFrame()
    updateHover()

    pos = getMousePos()

    if window.rightclick():
        if not SelectedNode1:
            if pos not in node_by_pos:
                name = ''.join(random.choice(string.ascii_letters) for _ in range(3))
                node = g_Node(name, pos)

                graph.AddUnConnected(node)
                node_by_pos[pos] = node
                displayGraph()
        else:
            node = node_by_pos.get(pos)

            if node:
                print("CONNECTING")
                graph.Add(SelectedNode1, node)
                displayGraph()

    if window.leftclick():
        if not SelectedNode1:
            node = node_by_pos.get(pos)

            if node:
                SelectedNode1 = node
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
