import pygame
import sys
import time

WIN = 400
CAPTION = 'A* path finding algorithm'
SCREEN = pygame.display.set_mode((WIN, WIN))
ROWS = 25

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (74, 116, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (196, 66, 219)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


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
        self.barrierPos = [(6, 12), (6, 18), (20, 11), (6, 15), (20, 14), (6, 21), (12, 16), (12, 19), (3, 16), (12, 22), (5, 16), (9, 11), (13, 5), (13, 11), (11, 11), (13, 8), (13, 14), (15, 11), (15, 14), (6, 11), (6, 14), (6, 20), (6, 17), (12, 15), (12, 21), (17, 11), (12, 18), (
            17, 14), (8, 11), (19, 11), (19, 14), (10, 11), (13, 7), (13, 10), (2, 16), (6, 13), (6, 16), (21, 14), (6, 19), (12, 11), (21, 11), (12, 14), (14, 11), (12, 17), (14, 14), (4, 16), (12, 20), (7, 11), (13, 9), (13, 6), (1, 16), (16, 14), (18, 11), (16, 11), (18, 14)]
        self.pathDict = {}
        self.pathFound = True

    def makeGrid(self):
        for i in range(ROWS):
            self.grid.append([])
            for j in range(ROWS):
                self.grid[i].append((j * self.gridSize, i * self.gridSize))
        # print(self.grid)

    def drawGrid(self):
        for i in range(ROWS):
            pygame.draw.line(SCREEN, BLACK, (0, self.grid[i][i][0]),
                             (WIN, self.grid[i][i][0]))
            for j in range(ROWS):
                pygame.draw.line(SCREEN, BLACK, (self.grid[i][j][1],
                                                 0), (self.grid[i][j][1], WIN))
        pygame.display.update()

    def draw(self, coord, colour):
        x, y = coord
        pygame.draw.rect(
            SCREEN, colour, (self.grid[x][y][1], self.grid[x][y][0], self.gridSize, self.gridSize))
        pygame.display.update()

    def h(self, start, end):
        x1, y1 = start
        x2, y2 = end
        return min(abs(x1 - x2), abs(y1 - y2)) * 14 + abs(abs(x1 - x2) - abs(y1 - y2)) * 10
        # return abs(y1 - y2) + abs(x1 - x2)
        # return int(math.sqrt(math.pow((y1 - y2), 2) + math.pow((x1 - x2), 2)) * 10)

    def g(self, start, currentCell):
        x1, y1 = start
        x2, y2 = currentCell
        # return abs(y1 - y2) + abs(x1 - x2)
        # return int(math.sqrt(math.pow((y1 - y2), 2) + math.pow((x1 - x2), 2)) * 10)
        return min(abs(x1 - x2), abs(y1 - y2)) * 14 + abs(abs(x1 - x2) - abs(y1 - y2)) * 10

    # Neighbours of parent cell, Column x Row
    # Right, Bottom-Right, Bottom, Bottom-Left, Left, Top-Left, Top, Top-Right,
    def algoNeighbours(self, cell):
        k = []
        n = [(cell[0] + 1, cell[1]), (cell[0] + 1, cell[1] + 1), (cell[0], cell[1] + 1), (cell[0] - 1, cell[1] + 1),
             (cell[0] - 1, cell[1]), (cell[0] - 1, cell[1] - 1), (cell[0], cell[1] - 1), (cell[0] + 1, cell[1] - 1)]
        for i in range(8):
            if n[i][0] >= 0 and n[i][1] >= 0 and n[i][0] < ROWS and n[i][1] < ROWS and n[i] not in self.barrierPos and n[i] != self.startCoord and n[i] not in self.pathDict:
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
                    # break
                else:
                    continue

    def algorithm(self):
        parentCell = self.startCoord
        costDict = {}
        neighboursDict = {}
        while parentCell != self.endCoord:
            children = self.algoNeighbours(parentCell)

            for i in range(len(children)):
                gCost = self.g(self.startCoord, children[i])
                hCost = self.h(children[i], self.endCoord)
                fCost = gCost + hCost

                if children[i] != self.endCoord:
                    self.draw(children[i], YELLOW)
                    self.drawGrid()
                costDict[children[i]] = [gCost, hCost, fCost]

            if costDict:
                tempFcost = min(data[2] for data in costDict.values())
                lowestF = [key for key, value in costDict.items()
                           if value[2] == tempFcost]

                parentCell = self.algoCalcultions(lowestF, costDict)
                if parentCell == self.endCoord:
                    break
                # self.visitedList.append(parentCell)
                self.pathDict[parentCell] = costDict.pop(parentCell)

            if parentCell != self.endCoord:
                self.draw(parentCell, WHITE)
            # pygame.display.update()
        self.reconstructPath(costDict)

    def reconstructNeighbours(self, cell, reversedPathDict):

        k = []
        n = [(cell[0] + 1, cell[1]), (cell[0] + 1, cell[1] + 1), (cell[0], cell[1] + 1), (cell[0] - 1, cell[1] + 1),
             (cell[0] - 1, cell[1]), (cell[0] - 1, cell[1] - 1), (cell[0], cell[1] - 1), (cell[0] + 1, cell[1] - 1)]
        for i in range(8):
            if n[i][0] >= 0 and n[i][1] >= 0 and n[i][0] < ROWS and n[i][1] < ROWS and n[i] not in self.barrierPos and n[i] != self.endCoord and n[i] in reversedPathDict:
                k.append(n[i])
            if n[i] == self.startCoord:
                k.append(n[i])
        return k

    def childrensNeighbours(self, cell, costDict):

        k = []
        n = [(cell[0] + 1, cell[1]), (cell[0] + 1, cell[1] + 1), (cell[0], cell[1] + 1), (cell[0] - 1, cell[1] + 1),
             (cell[0] - 1, cell[1]), (cell[0] - 1, cell[1] - 1), (cell[0], cell[1] - 1), (cell[0] + 1, cell[1] - 1)]
        for i in range(8):
            if n[i][0] >= 0 and n[i][1] >= 0 and n[i][0] < ROWS and n[i][1] < ROWS and n[i] not in self.barrierPos and n[i] != self.endCoord and n[i] in costDict:
                k.append(n[i])
            if n[i] == self.startCoord:
                k.append(n[i])
        return k

    def reconstructCalcultions(self, children, costDict):
        neigDict = {}
        for child in children:
            neigDict[child] = len(
                self.childrensNeighbours(child, costDict))
        tempCell = max(neigDict, key=neigDict.get)

        return tempCell

        # child = max(child for child in children if len(self.childrensNeighbours(child, costDict)) > 0)

    def reconstructPath(self, costDict):
        costDict = costDict
        reversedPathDict = {}
        donePath = False
        keysList = self.pathDict.keys()
        reversedKeysList = list(reversed(keysList))
        for key in reversedKeysList:
            reversedPathDict[key] = self.pathDict.pop(key)
        # print(reversedKeysList)
        # print(reversedPathDict)
        startCoordNeigh = self.reconstructNeighbours(
            self.startCoord, reversedPathDict)
        parentCell = reversedKeysList[0]
        while not donePath:
            self.draw(parentCell, PURPLE)
            self.drawGrid()
            children = []
            children = self.reconstructNeighbours(parentCell, reversedPathDict)
            if len(children) == 1:
                del reversedPathDict[parentCell]
                parentCell = children[0]

            else:
                del reversedPathDict[parentCell]
                parentCell = self.reconstructCalcultions(
                    children, costDict)
            # tempFcost = min(
            #     value[2] for key, value in reversedPathDict.items() if key in children or key == self.startCoord)
            # lowestF = [key for key, value in reversedPathDict.items()
            #            if value[2] == tempFcost and key in children or key == self.startCoord]
            # del reversedPathDict[parentCell]

            # parentCell = self.reconstructCalcultions(
            #     lowestF, reversedPathDict)
            # if parentCell in startCoordNeigh:
            #     self.draw(parentCell, PURPLE)
            #     self.drawGrid()
            #     donePath = True

    def coordCalculation(self, pos):
        x, y = pos
        x = x // self.gridSize
        y = y // self.gridSize
        return (x, y)

    def callEvent(self):
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            # print(event)
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
                    # self.barrierDone = False
                # elif not self.barrierDone:
                #     self.barriers = True
            # elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            #     x, y = event.pos
            #     x = x // self.gridSize
            #     y = y // self.gridSize
            #     if (x, y) == self.startCoord:
            #         self.startCoord = None
            #         self.drawPath((x, y), GREY)
            #         # self.drawStart(pygame.mouse.get_pos())
            #         self.startDone = False

        # if not keys[pygame.K_SPACE]:
        #     if self.barriers and pygame.mouse.get_pressed()[0] == 1:
        #         (x, y) = self.coordCalculation(pygame.mouse.get_pos())
        #         self.barrierPos.append((x, y))
        #         self.draw((x, y), BLACK)
        # else:
        # self.barriers = False
        # self.barrierDone = True
        # self.barrierPos = list(set(self.barrierPos))
            # print(self.barrierPos)
            if not self.pathFound:
                begin = time.process_time()
                self.algorithm()
                self.pathFound = True
                print('Time taken for execution: ' + str(begin))

        if keys[pygame.K_c]:
            SCREEN.fill(GREY)
            self.drawGrid()
            # # self.barrierDone = True
            # self.barriers = False
            self.startDone = False
            self.endDone = True
            # self.barrierPos = []
            self.pathFound = False
            self.pathDict = {}

    def mainLoop(self):
        SCREEN.fill(GREY)
        self.makeGrid()
        self.drawGrid()
        for i in self.barrierPos:
            self.draw(i, BLACK)
        while not self.done:
            self.callEvent()

            # pygame.display.update()


def main():
    pygame.init()
    pygame.display.set_caption(CAPTION)
    App().mainLoop()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
