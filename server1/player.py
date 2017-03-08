from ball import *


class Player:
    def __init__(self, name:str, balls:[Ball]):
        self.name = name
        self.balls = balls

    def move(self):
        for ball in self.balls:
            ball.move()

    def split(self):
        newBalls = []
        for ball in self.balls:
            if ball.size < PLAYER_START_SIZE * 2:
                newBalls.append(ball)
                continue
            (b1, b2) = ball.split()
            newBalls.append(b1)
            newBalls.append(b2)
        self.balls = newBalls

    @classmethod
    def random(classs, name:str, width:float, height:float):
        balls = [Ball.random(width, height, PLAYER_START_SIZE)]
        return classs(name, balls)

    def reprJSON(self):
        return self.__dict__.copy()

def testPlayer(printing=False):
    myPlayer = Player("Max", [testBall(False),testBall(False)])
    myPlayer.move()
    if printing: print(myPlayer.name, "== Max")
    if printing: print(myPlayer.balls[0].position.y, "== 5.0")
    if printing: print(Player.random("Max", 2000, 1000).balls[0].position.x, "== random")
    return myPlayer

if __name__ == '__main__':
    testPlayer(True)
