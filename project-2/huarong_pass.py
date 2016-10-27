"""
Introduction to Artificial Intelligence
Fall 2014
Author: Vishwanath Sangale
"""

import search
import datetime


class HuarongPass(search.Problem):
    def __init__(self):
        self.initial = (('A', 'B', 'B', 'C'),
                        ('A', 'B', 'B', 'C'),
                        ('D', 'E', 'E', 'F'),
                        ('D', 'G', 'H', 'F'),
                        ('I', 'X', 'X', 'J'))

        """33rd move"""
        """self.initial = (('B', 'B', 'A', 'G'),
                        ('B', 'B', 'A', 'H'),
                        ('F', 'C', 'D', 'X'),
                        ('F', 'C', 'D', 'X'),
                        ('I', 'J', 'E', 'E'))"""
        """47th move"""
        """self.initial = (('F', 'G', 'H', 'I'),
                        ('F', 'B', 'B', 'D'),
                        ('C', 'B', 'B', 'D'),
                        ('C', 'J', 'A', 'X'),
                        ('E', 'E', 'A', 'X'))"""
        """57th move"""
        """self.initial = (('C', 'F', 'G', 'D'),
                        ('C', 'F', 'H', 'D'),
                        ('B', 'B', 'X', 'X'),
                        ('B', 'B', 'I', 'A'),
                        ('E', 'E', 'J', 'A'))"""
        """67th move"""
        """self.initial = (('F', 'G', 'D', 'A'),
                        ('F', 'H', 'D', 'A'),
                        ('C', 'B', 'B', 'X'),
                        ('C', 'B', 'B', 'X'),
                        ('E', 'E', 'I', 'J'))"""
        """74th move"""
        """self.initial = (('C', 'F', 'D', 'A'),
                        ('C', 'F', 'D', 'A'),
                        ('G', 'H', 'B', 'B'),
                        ('E', 'E', 'B', 'B'),
                        ('X', 'X', 'I', 'J'))"""
        self.minimumLengthOfRow = 0
        self.maximumLengthOfRow = 5
        self.minimumLengthOfColumn = 0
        self.maximumLengthOfColumn = 4
        self.multipleGridNodes = dict(
            [('A', '2x1'), ('B', '2x2'), ('C', '2x1'), ('D', '2x1'), ('E', '1x2'), ('F', '2x1'), ('G', '1x1'),
             ('H', '1x1'), ('I', '1x1'), ('J', '1x1')])

    def findEmptyTiles(self, state):
        """Returns the locations of empty tiles.
        :param state:
        """
        emptyTiles = []
        for x in range(self.minimumLengthOfRow, self.maximumLengthOfRow):
            for y in range(self.minimumLengthOfColumn, self.maximumLengthOfColumn):
                if state[x][y] == 'X':
                    emptyTiles.append((x, y))
                if state[x][y] == 'X':
                    emptyTiles.append((x, y))
        return emptyTiles

    def getAdjacentNodes(self, x, y):
        adjacentNodes = []
        if x < 4:
            adjacentNodes.append(((x + 1, y), 'UP'))
        if x > 0:
            adjacentNodes.append(((x - 1, y), 'DOWN'))
        if y < 3:
            adjacentNodes.append(((x, y + 1), 'LEFT'))
        if y > 0:
            adjacentNodes.append(((x, y - 1), 'RIGHT'))
        return adjacentNodes

    def checkIfNodesAreMovable(self, state, adjacentNodes):
        movableAdjacentNodes = []
        for nodes in adjacentNodes:
            x, y = adjacentNodes[adjacentNodes.index(nodes)][0]
            element = state[x][y]
            if element == 'X':
                continue
            if self.multipleGridNodes[element] == '1x1':
                movableAdjacentNodes += ((element, adjacentNodes[adjacentNodes.index(nodes)][1]),)
            elif self.multipleGridNodes[element] == '2x1':
                if adjacentNodes[adjacentNodes.index(nodes)][1] == 'UP' and element == state[x + 1][y]:
                    movableAdjacentNodes += ((element, adjacentNodes[adjacentNodes.index(nodes)][1]),)
                elif adjacentNodes[adjacentNodes.index(nodes)][1] == 'DOWN' and element == state[x - 1][y]:
                    movableAdjacentNodes += ((element, adjacentNodes[adjacentNodes.index(nodes)][1]),)
                elif adjacentNodes[adjacentNodes.index(nodes)][1] == 'LEFT':
                    if x + 1 <= 4 and state[x + 1][y - 1] == 'X' and element == state[x + 1][y]:
                        movableAdjacentNodes += ((element, adjacentNodes[adjacentNodes.index(nodes)][1]),)
                elif adjacentNodes[adjacentNodes.index(nodes)][1] == 'RIGHT':
                    if x + 1 <= 4 and state[x + 1][y + 1] == 'X' and element == state[x + 1][y]:
                        movableAdjacentNodes += ((element, adjacentNodes[adjacentNodes.index(nodes)][1]),)
            elif self.multipleGridNodes[element] == '1x2' and y < 3 and element == state[x][y + 1]:
                if adjacentNodes[adjacentNodes.index(nodes)][1] == 'UP':
                    if state[x - 1][y + 1] == 'X':
                        movableAdjacentNodes += ((element, adjacentNodes[adjacentNodes.index(nodes)][1]),)
                elif adjacentNodes[adjacentNodes.index(nodes)][1] == 'DOWN':
                    if state[x + 1][y + 1] == 'X':
                        movableAdjacentNodes += ((element, adjacentNodes[adjacentNodes.index(nodes)][1]),)
                elif adjacentNodes[adjacentNodes.index(nodes)][1] == 'LEFT':
                    movableAdjacentNodes += ((element, adjacentNodes[adjacentNodes.index(nodes)][1]),)
                elif adjacentNodes[adjacentNodes.index(nodes)][1] == 'RIGHT':
                    movableAdjacentNodes += ((element, adjacentNodes[adjacentNodes.index(nodes)][1]),)
            elif self.multipleGridNodes[element] == '2x2':
                if adjacentNodes[adjacentNodes.index(nodes)][1] == 'UP':
                    if y < 3 and state[x][y + 1] == state[x][y]:
                        if x > 0 and state[x - 1][y + 1] == 'X':
                            movableAdjacentNodes += ((element, adjacentNodes[adjacentNodes.index(nodes)][1]),)
                    elif y > 0 and state[x][y - 1] == state[x][y]:
                        if x > 0 and state[x - 1][y - 1] == 'X':
                            movableAdjacentNodes += ((element, adjacentNodes[adjacentNodes.index(nodes)][1]),)
                elif adjacentNodes[adjacentNodes.index(nodes)][1] == 'DOWN':
                    if y < 3 and state[x][y + 1] == state[x][y]:
                        if x < 4 and state[x + 1][y + 1] == 'X':
                            movableAdjacentNodes += ((element, adjacentNodes[adjacentNodes.index(nodes)][1]),)
                    elif y > 0 and state[x][y - 1] == state[x][y]:
                        if x < 4 and state[x + 1][y - 1] == 'x':
                            movableAdjacentNodes += ((element, adjacentNodes[adjacentNodes.index(nodes)][1]),)
                elif adjacentNodes[adjacentNodes.index(nodes)][1] == 'LEFT':
                    if x > 0 and state[x - 1][y] == state[x][y]:
                        if y > 0 and state[x - 1][y - 1] == 'X':
                            movableAdjacentNodes += ((element, adjacentNodes[adjacentNodes.index(nodes)][1]),)
                    elif x < 4 and state[x + 1][y] == state[x][y]:
                        if y > 0 and state[x + 1][y - 1] == 'X':
                            movableAdjacentNodes += ((element, adjacentNodes[adjacentNodes.index(nodes)][1]),)
                elif adjacentNodes[adjacentNodes.index(nodes)][1] == 'RIGHT':
                    if x < 4 and state[x + 1][y] == state[x][y]:
                        if y < 3 and state[x + 1][y + 1] == 'X':
                            movableAdjacentNodes += ((element, adjacentNodes[adjacentNodes.index(nodes)][1]),)
                    elif x > 0 and state[x][y] == state[x - 1][y]:
                        if y < 3 and state[x - 1][y + 1] == 'X':
                            movableAdjacentNodes += ((element, adjacentNodes[adjacentNodes.index(nodes)][1]),)
        return movableAdjacentNodes

    def findAdjacentMovableNodesOfEmptyTiles(self, state, emptyTiles):
        """Returns the list of movable nodes adjacent to empty tiles.
        In the format ((x,y),DIR).
        :rtype : object
        :param state:
        :param emptyTiles:
        """
        x1, y1 = emptyTiles[0]
        x2, y2 = emptyTiles[1]
        adjacentNodes = self.getAdjacentNodes(x2, y2)
        adjacentNodes += self.getAdjacentNodes(x1, y1)
        return self.checkIfNodesAreMovable(state, adjacentNodes)

    def actions(self, state):
        """Returns a Python list that contains the possible actions from
        the given state."""
        emptyTiles = self.findEmptyTiles(state)
        movableAdjacentNodes = self.findAdjacentMovableNodesOfEmptyTiles(state, emptyTiles)
        return movableAdjacentNodes

    def result(self, state, action):
        """Returns the state that results from applying the given
        action to the given state."""
        node, actualAction = action
        givenState = [list(row) for row in state]
        for x in range(self.minimumLengthOfRow, self.maximumLengthOfRow):
            for y in range(self.minimumLengthOfColumn, self.maximumLengthOfColumn):
                element = state[x][y]
                if element == node:
                    if self.multipleGridNodes[element] == '1x1':
                        if actualAction == 'UP':
                            givenState[x - 1][y] = node
                        elif actualAction == 'DOWN':
                            givenState[x + 1][y] = node
                        elif actualAction == 'LEFT':
                            givenState[x][y - 1] = node
                        elif actualAction == 'RIGHT':
                            givenState[x][y + 1] = node
                        givenState[x][y] = 'X'
                        return tuple(tuple(row) for row in givenState)
                    elif self.multipleGridNodes[element] == '1x2':
                        if actualAction == 'UP':
                            givenState[x - 1][y] = node
                            givenState[x - 1][y + 1] = node
                            givenState[x][y + 1] = 'X'
                            givenState[x][y] = 'X'
                            return tuple(tuple(row) for row in givenState)
                        elif actualAction == 'DOWN':
                            givenState[x + 1][y] = node
                            givenState[x + 1][y + 1] = node
                            givenState[x][y + 1] = 'X'
                            givenState[x][y] = 'X'
                            # print "SAC", givenState
                        elif actualAction == 'LEFT':
                            givenState[x][y - 1] = node
                            givenState[x][y + 1] = 'X'
                            return tuple(tuple(row) for row in givenState)
                        elif actualAction == 'RIGHT':
                            givenState[x][y + 1] = node
                            givenState[x][y - 1] = 'X'
                            return tuple(tuple(row) for row in givenState)
                    elif self.multipleGridNodes[element] == '2x1':
                        if actualAction == 'UP':
                            givenState[x - 1][y] = node
                            givenState[x + 1][y] = 'X'
                            return tuple(tuple(row) for row in givenState)
                        elif actualAction == 'DOWN':
                            givenState[x + 2][y] = node
                            givenState[x][y] = 'X'
                            return tuple(tuple(row) for row in givenState)
                        elif actualAction == 'LEFT':
                            givenState[x][y - 1] = node
                            givenState[x + 1][y - 1] = node
                            givenState[x + 1][y] = 'X'
                            givenState[x][y] = 'X'
                            return tuple(tuple(row) for row in givenState)
                        elif actualAction == 'RIGHT':
                            givenState[x][y + 1] = node
                            givenState[x + 1][y + 1] = node
                            givenState[x + 1][y] = 'X'
                            givenState[x][y] = 'X'
                            return tuple(tuple(row) for row in givenState)
                    elif self.multipleGridNodes[element] == '2x2':
                        if actualAction == 'UP':
                            givenState[x - 1][y] = node
                            givenState[x - 1][y + 1] = node
                            givenState[x + 1][y] = 'X'
                            givenState[x + 1][y + 1] = 'X'
                            return tuple(tuple(row) for row in givenState)
                        elif actualAction == 'DOWN':
                            givenState[x + 2][y] = node
                            givenState[x + 2][y + 1] = node
                            givenState[x][y] = 'X'
                            givenState[x][y + 1] = 'X'
                            return tuple(tuple(row) for row in givenState)
                        elif actualAction == 'LEFT':
                            givenState[x][y - 1] = node
                            givenState[x + 1][y - 1] = node
                            givenState[x][y + 1] = 'X'
                            givenState[x + 1][y + 1] = 'X'
                            return tuple(tuple(row) for row in givenState)
                        elif actualAction == 'RIGHT':
                            givenState[x][y + 2] = node
                            givenState[x + 1][y + 2] = node
                            givenState[x + 1][y] = 'X'
                            givenState[x][y] = 'X'
                            return tuple(tuple(row) for row in givenState)
        return tuple(tuple(row) for row in givenState)

    def goal_test(self, state):
        """tests whether the given state is a goal state, i.e. that Cao
        Cao is in the middle of the bottom row."""
        # print state
        if state[4][1] == 'B' and state[4][2] == 'B':
            return True
        else:
            return False


def huarong_pass_search(desired_search_strategy):
    """The function returns a list of actions that when applied to the initial state lead to the goal
    state."""
    initTime = datetime.datetime.now()
    problem = HuarongPass()
    if desired_search_strategy == "BFS":
        s = search.breadth_first_tree_search(problem)
    elif desired_search_strategy == "DFS":
        s = search.depth_first_graph_search(problem)
    elif desired_search_strategy == "IDS":
        s = search.iterative_deepening_search(problem)
    else:
        print "Desired search strategy not found!"
    endTime = datetime.datetime.now()
    print "Time taken", endTime - initTime
    return s.solution()
