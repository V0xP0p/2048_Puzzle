from Grid_3 import Grid
from ComputerAI_3 import ComputerAI
from PlayerAI_Final_Working import PlayerAI
from Displayer_3 import Displayer
from random import randint
import time
import itertools

defaultInitialTiles = 2
defaultProbability = 0.9

actionDic = {
    0: "UP",
    1: "DOWN",
    2: "LEFT",
    3: "RIGHT"
}

(PLAYER_TURN, COMPUTER_TURN) = (0, 1)

# Time Limit Before Losing
timeLimit = 0.2
allowance = 0.05


class GameManager:
    def __init__(self, size = 4):
        self.grid = Grid(size)
        self.possibleNewTiles = [2, 4]
        self.probability = defaultProbability
        self.initTiles  = defaultInitialTiles
        self.computerAI = None
        self.playerAI   = None
        self.displayer  = None
        self.over       = False

    def setComputerAI(self, computerAI):
        self.computerAI = computerAI

    def setPlayerAI(self, playerAI):
        self.playerAI = playerAI

    def setDisplayer(self, displayer):
        self.displayer = displayer

    def updateAlarm(self, currTime):
        if currTime - self.prevTime > timeLimit + allowance:
            self.over = True
            print("TIME IS UP")
            pass
        else:
            while time.clock() - self.prevTime < timeLimit + allowance:
                pass

            self.prevTime = time.clock()

    def start(self, w1, w2, w3):
        for i in range(self.initTiles):
            self.insertRandonTile()

        self.displayer.display(self.grid)

        # Player AI Goes First
        turn = PLAYER_TURN
        maxTile = 0

        self.prevTime = time.clock()

        while not self.isGameOver() and not self.over:
            # Copy to Ensure AI Cannot Change the Real Grid to Cheat
            gridCopy = self.grid.clone()

            move = None

            if turn == PLAYER_TURN:
                print("Player's Turn:", end="")
                move = self.playerAI.getMove(gridCopy, w1, w2, w3)
                print(actionDic[move])

                # Validate Move
                if move != None and move >= 0 and move < 4:
                    if self.grid.canMove([move]):
                        self.grid.move(move)

                        # Update maxTile
                        maxTile = self.grid.getMaxTile()
                    else:
                        print("Invalid PlayerAI Move")
                        self.over = True
                else:
                    print("Invalid PlayerAI Move - 1")
                    self.over = True
            else:
                print("Computer's turn:")
                move = self.computerAI.getMove(gridCopy)

                # Validate Move
                if move and self.grid.canInsert(move):
                    self.grid.setCellValue(move, self.getNewTileValue())
                else:
                    print("Invalid Computer AI Move")
                    self.over = True

            if not self.over:
                self.displayer.display(self.grid)

            # Exceeding the Time Allotted for Any Turn Terminates the Game
            self.updateAlarm(time.clock())

            turn = 1 - turn
        print(maxTile)
        return maxTile

    def isGameOver(self):
        return not self.grid.canMove()

    def getNewTileValue(self):
        if randint(0,99) < 100 * self.probability:
            return self.possibleNewTiles[0]
        else:
            return self.possibleNewTiles[1]

    def insertRandonTile(self):
        tileValue = self.getNewTileValue()
        cells = self.grid.getAvailableCells()
        cell = cells[randint(0, len(cells) - 1)]
        self.grid.setCellValue(cell, tileValue)

def main():


    w = [100, 10]

    max_iterations = 2
    average_score = 0
    score_list = []

    iter_list = [1, 10, 50, 100, 1000]
    # w = [10000, 1000, 10, 1500, 5000]
    max_score = 0   # [-1, (0, 0, 0, 0)]
    max_average = 0  # [-1, (0, 0, 0, 0)]

    f = open('output.txt', 'w')

    counter = 0

    for w3 in iter_list:     # itertools.product(iter_list, repeat=1):
        iterations = 0
        while iterations < max_iterations:

            gameManager = GameManager()
            playerAI = PlayerAI()
            computerAI = ComputerAI()
            displayer = Displayer()

            gameManager.setDisplayer(displayer)
            gameManager.setPlayerAI(playerAI)
            gameManager.setComputerAI(computerAI)

            score = gameManager.start(w[0], w[1], w3)

            max_score = max(max_score, score)

            average_score += max_score

            score_list.append(score)

            iterations += 1
            counter += 1

        f.write(str(counter) + "    " + str(score) + " " + "[" + str(w[0]) + "," + str(w[1]) + "," + str(w3) + "]" + '\n')

    average_score /= max_iterations

    max_average = max(max_average, average_score)

    print(max_average, score_list)
    f.close()


if __name__ == '__main__':
    main()
