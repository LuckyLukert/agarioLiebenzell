from ball import *


class Player:
    def __init__(self, name:str, color:str, balls:[Ball]):
        self.name = name
        self.color = color
        self.balls = balls

    def move(self):
        for ball in self.balls:
            ball.move()


def testPlayer(printing=False):
    myPlayer = Player("Max", "0xFF00FF", [testBall(False),testBall(False)])
    myPlayer.move()
    if printing: print(myPlayer.name, "== Max")
    if printing: print(myPlayer.balls[0].position.y, "== 5.0")
    return myPlayer

if __name__ == '__main__':
    testPlayer(True)
