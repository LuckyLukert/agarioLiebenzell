from ball import *


class Player:
    def __init__(self, name:str, color:str, balls:[Ball]):
        self.name = name
        self.color = color
        self.balls = balls


def testPlayer(printing=False):
    myPlayer = Player("Max", "0xFF00FF", [testBall(False),testBall(False)])
    if printing: print(myPlayer.name)
    if printing: print(myPlayer.balls[0].size)
    return myPlayer

if __name__ == '__main__':
    testPlayer(True)
