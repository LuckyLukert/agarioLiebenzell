from ball import *


class Player:
    def __init__(self, name:str, color:str, balls:[Ball]):
        self.name = name
        self.color = color
        self.balls = balls

    def move(self):
        for ball in self.balls:
            ball.move()

    @classmethod
    def random(classs, name:str, color:str, width:float, height:float):
        balls = [Ball.random(width, height, 10)]
        return classs(name, color, balls)

    def reprJSON(self):
        return __dict__.copy()

def testPlayer(printing=False):
    myPlayer = Player("Max", "0xFF00FF", [testBall(False),testBall(False)])
    myPlayer.move()
    if printing: print(myPlayer.name, "== Max")
    if printing: print(myPlayer.balls[0].position.y, "== 5.0")
    if printing: print(Player.random("Max", "0xFF0000", 2000, 1000).balls[0].position.x, "== random")
    return myPlayer

if __name__ == '__main__':
    testPlayer(True)
