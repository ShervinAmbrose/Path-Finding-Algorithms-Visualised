import pygame
import sys
import math
import random
'''
Change this to change the screen size and number of boxes
recommended is WIN = 800, ROWS = 50
you can aslo change it to WIN = 400, ROWS = 25
'''
WIN = 800
ROWS = 50

CAPTION = 'A* path finding algorithm'
SCREEN = pygame.display.set_mode((WIN, WIN))

'''Number of parentCell neighbours, Choose 4 or 8 only.
Each cell can either have 4 neighbours (Right, Bottom, Left, Top)
Or 8 neighbours (Right, Bottom-Right, Bottom, Bottom-Left, Left, Top-Left, Top, Top-Right)
Recommended is 8
'''
neigh = 4


GREEN = (0, 255, 0)
PURPLE = (255, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

'''
Main Class for entire code
'''


class App(object):
    def __init__(self):
        self.done = False
        self.grid = []
        self.gridSize = WIN // ROWS
        self.startDone = False
        self.endDone = True
        self.barrierDone = True
        self.barriers = False
        self.startCoord = None
        self.endCoord = None
        self.barrierPos = []
        self.pathDict = {}
        self.pathFound = True
        self.removeBarrier = []

    '''
    Stores the (x, y) co-ordinates
    '''

    def makeGrid(self):
        for i in range(ROWS):
            self.grid.append([])
            for j in range(ROWS):
                self.grid[i].append((j * self.gridSize, i * self.gridSize))
        self.drawGrid()

    '''
    Draws vertical and horizontal line on the (x, y) co-ordinates
    '''

    def drawGrid(self):
        for i in range(ROWS):
            pygame.draw.line(
                SCREEN, BLACK, (0, self.grid[i][i][0]), (WIN, self.grid[i][i][0]))
            for j in range(ROWS):
                pygame.draw.line(
                    SCREEN, BLACK, (self.grid[i][j][1], 0), (self.grid[i][j][1], WIN))
        pygame.display.update()

    '''
    One draw Function to draw the start, end, barriers, erase-bariers and the output path.
    '''

    def draw(self, coord, colour):
        x, y = coord
        pygame.draw.rect(
            SCREEN, colour, (self.grid[x][y][1], self.grid[x][y][0], self.gridSize, self.gridSize))
        pygame.display.update()
        self.drawGrid()

    '''
    Different H and G scores to play with
    '''

    def h(self, start, end):
        x1, y1 = start
        x2, y2 = end
        # return abs(y1 - y2) + abs(x1 - x2)
        return min(abs(x1 - x2), abs(y1 - y2)) * 14 + abs(abs(x1 - x2) - abs(y1 - y2)) * 10

    def g(self, start, currentCell):
        x1, y1 = start
        x2, y2 = currentCell
        # return abs(y1 - y2) + abs(x1 - x2)
        return min(abs(x1 - x2), abs(y1 - y2)) * 14 + abs(abs(x1 - x2) - abs(y1 - y2)) * 10

    '''Neighbours of parent cell, Column x Row'''

    def algoNeighbours(self, cell):
        k = []
        if neigh == 8:
            n = [(cell[0] + 1, cell[1]), (cell[0] + 1, cell[1] + 1), (cell[0], cell[1] + 1), (cell[0] - 1, cell[1] + 1),
                 (cell[0] - 1, cell[1]), (cell[0] - 1, cell[1] - 1), (cell[0], cell[1] - 1), (cell[0] + 1, cell[1] - 1)]
        elif neigh == 4:
            n = [(cell[0] + 1, cell[1]), (cell[0], cell[1] + 1),
                 (cell[0] - 1, cell[1]), (cell[0], cell[1] - 1)]
        for i in range(neigh):
            if n[i][0] >= 0 and n[i][1] >= 0 and n[i][0] < ROWS and n[i][1] < ROWS and n[i] not in self.barrierPos and n[i] != self.startCoord and n[i] not in self.pathDict:
                k.append(n[i])
        return k

    def reconstructNeighbours(self, cell, cellDict):
        k = []
        if neigh == 8:
            n = [(cell[0] + 1, cell[1]), (cell[0] + 1, cell[1] + 1), (cell[0], cell[1] + 1), (cell[0] - 1, cell[1] + 1),
                 (cell[0] - 1, cell[1]), (cell[0] - 1, cell[1] - 1), (cell[0], cell[1] - 1), (cell[0] + 1, cell[1] - 1)]
        elif neigh == 4:
            n = [(cell[0] + 1, cell[1]), (cell[0], cell[1] + 1),
                 (cell[0] - 1, cell[1]), (cell[0], cell[1] - 1)]
        for i in range(neigh):
            if n[i][0] >= 0 and n[i][1] >= 0 and n[i][0] < ROWS and n[i][1] < ROWS and n[i] not in self.barrierPos and n[i] in self.pathDict and n[i] not in cellDict:
                k.append(n[i])
            if n[i] == self.endCoord:
                k.append(n[i])
        return k

    def reconstructPath(self, cell):
        k = []
        if neigh == 8:
            n = [(cell[0] + 1, cell[1]), (cell[0] + 1, cell[1] + 1), (cell[0], cell[1] + 1), (cell[0] - 1, cell[1] + 1),
                 (cell[0] - 1, cell[1]), (cell[0] - 1, cell[1] - 1), (cell[0], cell[1] - 1), (cell[0] + 1, cell[1] - 1)]
        elif neigh == 4:
            n = [(cell[0] + 1, cell[1]), (cell[0], cell[1] + 1),
                 (cell[0] - 1, cell[1]), (cell[0], cell[1] - 1)]
        for i in range(neigh):
            if n[i][0] >= 0 and n[i][1] >= 0 and n[i][0] < ROWS and n[i][1] < ROWS and n[i] not in self.barrierPos and n[i] in self.pathDict:
                k.append(n[i])
        return k

    def algoCalcultions(self, lowestF, costDict):
        if len(lowestF) == 1:
            return lowestF[0]
        else:
            tempHcost = min(value[1]
                            for key, value in costDict.items() if key in lowestF)
            for key in lowestF:
                data = costDict[key]
                if data[1] == tempHcost:
                    return key
                else:
                    continue

    '''
    Basic working of algorithm is that it takes the starting cell as parentCell and determines its
    neighbours(children), the G, H and F cost of each neighbour is calculated and the neighbour
    with lowest F cost becomes the new parent cell, this process is repeated until the parentCell
    is equal to the endCoordinate.
    '''

    def algorithm(self):
        parentCell = self.startCoord
        costDict = {}
        while parentCell != self.endCoord:
            children = self.algoNeighbours(parentCell)
            for i in range(len(children)):
                gCost = self.g(self.startCoord, children[i])
                hCost = self.h(children[i], self.endCoord)
                fCost = gCost + hCost

                if children[i] != self.endCoord:
                    self.draw(children[i], YELLOW)
                costDict[children[i]] = [gCost, hCost, fCost]
            if costDict:
                tempFcost = min(data[2] for data in costDict.values())
                lowestF = [key for key, value in costDict.items()
                           if value[2] == tempFcost]

                parentCell = self.algoCalcultions(lowestF, costDict)
                if parentCell == self.endCoord:
                    break
                self.pathDict[parentCell] = costDict.pop(parentCell)
            else:
                self.noSolution()
            if parentCell != self.endCoord:
                self.draw(parentCell, WHITE)
        '''
        Once the cells from start to end are explored,
        each explored cell is assigned a number
        '''
        number = 1
        parentCell = self.startCoord
        cellDict = {}
        children = self.reconstructNeighbours(parentCell, cellDict)
        for child in children:
            cellDict[child] = number
            number += 1
        cell = 1
        while parentCell != self.endCoord:
            parentCell = [key for key, value in cellDict.items()
                          if value == cell]
            children = self.reconstructNeighbours(parentCell[0], cellDict)
            if len(children) > 0 and children[0] == self.endCoord:
                break
            for child in children:
                cellDict[child] = number
                # self.draw(child, PURPLE)
                number += 1
            cell += 1
        '''
        After assigning numbers to each cell,
        the path from end to star is determined by
        choosing the endCell as parentCell, then determining
        its neighbours and choosing the neighbour with lowest
        number as the new parent cell
        '''
        donePath = False
        startCoordNeigh = self.reconstructPath(self.startCoord)
        reversedCellDict = {}
        keysList = cellDict.keys()
        reversedKeysList = list(reversed(keysList))
        for key in reversedKeysList:
            reversedCellDict[key] = cellDict.pop(key)
        endCoordNeigh = self.reconstructPath(self.endCoord)
        for key in reversedKeysList:
            if key in endCoordNeigh:
                parentCell = key
                break
        while not donePath:
            self.draw(parentCell, PURPLE)
            children = []
            children = self.reconstructPath(parentCell)
            if len(children) == 1:
                del reversedCellDict[parentCell]
                del self.pathDict[parentCell]
                parentCell = children[0]
            else:
                del reversedCellDict[parentCell]
                del self.pathDict[parentCell]
                temp = min(
                    value for key, value in reversedCellDict.items() if key in children)
                tempCell = [key for key,
                            value in reversedCellDict.items() if value == temp]
                parentCell = tempCell[0]
            if parentCell in startCoordNeigh:
                self.draw(parentCell, PURPLE)
                donePath = True
    '''
    Takes the mouse (x, y) position and converts it to
    the grid's (x, y) coordinate
    '''

    def coordCalculation(self, pos):
        x, y = pos
        x = x // self.gridSize
        y = y // self.gridSize
        return (x, y)
    '''
    If no solution is found press escape or the cross mark
    '''

    def noSolution(self):
        running = True
        keys = pygame.key.get_pressed()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                    running = False
                    pygame.quit()
                    sys.exit()
    '''
    An event loop for calling start, end and barrier.
    '''

    def callEvent(self):
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                self.done = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not self.startDone:
                    self.startCoord = self.coordCalculation(event.pos)
                    self.draw(self.startCoord, GREEN)
                    self.startDone = True
                    self.endDone = False
                elif not self.endDone:
                    self.endCoord = self.coordCalculation(event.pos)
                    self.draw(self.endCoord, TURQUOISE)
                    self.endDone = True
                    self.pathFound = False
                    self.barrierDone = False
                elif not self.barrierDone:
                    self.barriers = True
        if pygame.mouse.get_pressed()[2] == 1:
            (x, y) = self.coordCalculation(pygame.mouse.get_pos())
            if (x, y) != self.startCoord and (x, y) != self.endCoord:
                self.removeBarrier.append((x, y))
                self.draw((x, y), GREY)
                self.barrierPos = list(
                    set(self.barrierPos) - set(self.removeBarrier))
                self.removeBarrier = []

        if not keys[pygame.K_SPACE]:
            if self.barriers and pygame.mouse.get_pressed()[0] == 1:
                (x, y) = self.coordCalculation(pygame.mouse.get_pos())
                self.barrierPos.append((x, y))
                self.draw((x, y), BLACK)
                self.barrierPos = list(
                    set(self.barrierPos) - set(self.removeBarrier))
                self.removeBarrier = []
        else:
            self.barriers = False
            self.barrierDone = True
            if not self.pathFound:
                self.algorithm()
                self.pathFound = True
        '''
        Press 'c' to clear the display and start over again
        '''
        if keys[pygame.K_c]:
            SCREEN.fill(GREY)
            self.makeGrid()
            self.barrierDone = True
            self.barriers = False
            self.startDone = False
            self.endDone = True
            self.barrierPos = []
            self.pathFound = False
            self.pathDict = {}
            self.removeBarrier = []

        if keys[pygame.K_r]:
            for i in range((ROWS * ROWS) // 4):
                x = random.randint(0, ROWS - 1)
                y = random.randint(0, ROWS - 1)
                if (x, y) != self.startCoord and (x, y) != self.endCoord:
                    self.barrierPos.append((x, y))
                    self.draw((x, y), BLACK)

    def mainLoop(self):
        SCREEN.fill(GREY)
        self.makeGrid()
        while not self.done:
            self.callEvent()


def main():
    pygame.init()
    pygame.display.set_caption(CAPTION)
    App().mainLoop()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
