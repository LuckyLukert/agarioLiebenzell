from player import *
from ball import *


class World:
    def __init__(self, food:{int:Ball}, obstacles:{int:Ball}, players:{int:Player}, width:int, height:int):
        self.food = food
        self.obstacles = obstacles
        self.players = players
        self.width = width
        self.height = height


def testWorld(printing = False):
    player1 = testPlayer()
    player2 = testPlayer()
    playerDict = {1:player1, 2:player2}
    obstacle = testBall()
    food = testBall()

    myWorld = World({1:food}, {1:obstacle}, playerDict, 3, 4)
    if printing: print(myWorld.players[1].name)

    return myWorld


if __name__ == '__main__':
    testWorld(True)
