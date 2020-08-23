import math


class Action:
    up = 1
    down = 2
    left = 3
    right = 4

    def __init__(self, direction):
        self.direction = direction


class State:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Node:
    def __init__(self, parent, state, action, depth):
        self.parent = parent
        self.state = state
        self.action = action
        self.depth = depth


goal = State(11, 0)
initialState = State(0, 6)
exploredSet = []
maze = [
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
    [1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
]


def heuristic(node):
    return node.depth + math.sqrt(pow(goal.x - node.state.x, 2) + pow(goal.y - node.state.y, 2))


def goal_test(state):
    return state.x == goal.x and state.y == goal.y


def result(state, action):
    nState = State(state.x, state.y)
    if action == Action.up:
        nState.y = nState.y - 1
    if action == Action.down:
        nState.y = nState.y + 1
    if action == Action.left:
        nState.x = nState.x - 1
    if action == Action.right:
        nState.x = nState.x + 1
    return nState


def actions(state, maze):
    actions = []  # Contains possible actions
    if state.x >= 0 and state.x < len(maze[0]):
        if state.y >= 0 and state.y < len(maze):
            ''' Pode ir para cima? '''
            if state.y - 1 >= 0 and maze[state.y-1][state.x] == 0:
                actions.append(Action.up)
            ''' Pode ir para baixo ? '''
            if state.y + 1 < len(maze) and maze[state.y + 1][state.x] == 0:
                actions.append(Action.down)
            ''' Pode ir para direita? '''
            if state.x + 1 < len(maze[0]) and maze[state.y][state.x+1] == 0:
                actions.append(Action.right)
            ''' Pode ir para esquerda? '''
            if state.x - 1 >= 0 and maze[state.y][state.x-1] == 0:
                actions.append(Action.left)
    return actions


def expand(node, maze):
    nodes = []
    theactions = actions(node.state, maze)
    for action in theactions:
        nodes.append(
            Node(node, result(node.state, action), action, node.depth + 1))
    return nodes


def printMaze(maze):
    for r in maze:
        for c in r:
            if c == 0:
                print("🌫️", end='')
            if c == 1:
                print("🔳", end='')
            if c == 6:
                print("👽", end='')
        print()


def printPath(node):
    while node != None:
        maze[node.state.y][node.state.x] = 6
        node = node.parent
    printMaze(maze)


def printExploredNodes(exploredSet, maze):
    for r in range(len(maze)):
        for c in range(len(maze[0])):
            found = False
            for n in exploredSet:
                if r == n.state.y and c == n.state.x:
                    found = True
                    break
            if not found:
                if maze[r][c] == 0:
                    print("🌫️", end='')
                if maze[r][c] == 1:
                    print("🔳", end='')
                if maze[r][c] == 6:
                    print("👽", end='')
            else:
                print("💡", end='')
        print()


def inExploredSet(node):
    for n in exploredSet:
        if n.state.x == node.state.x:
            if n.state.y == node.state.y:
                return True
    return False


'''
Retorna heuristicamente o indice do Node mais próximo do objetivo no frontier
'''


def getNodeByHeuristic(frontier):
    bestHeuristic = 0
    for index in range(len(frontier)):
        if heuristic(frontier[index]) < heuristic(frontier[bestHeuristic]):
            bestHeuristic = index
    return bestHeuristic


def bfs(initialState, maze):
    frontier = [Node(None, initialState, None, 0)]
    while True:
        if len(frontier) == 0:
            print("No solution")
            return
        nodeFrontier = frontier.pop(getNodeByHeuristic(frontier))
        exploredSet.append(nodeFrontier)
        if goal_test(nodeFrontier.state):
            printPath(nodeFrontier)
            break
        nodes = expand(nodeFrontier, maze)
        for node in nodes:
            if not inExploredSet(node):
                frontier.append(node)


print("-- The maze --")
printMaze(maze)

print("-- The solution --")
bfs(initialState, maze)

print("{} explored nodes".format(len(exploredSet)))
printExploredNodes(exploredSet, maze)
