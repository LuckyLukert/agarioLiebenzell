from player import *
from ball import *


class World:
    def __init__(self, food:{int:Ball}, obstacles:{int:Ball}, players:{int:Player}, width:float, height:float):
        self.food = food
        self.obstacles = obstacles
        self.players = players
        self.width = width
        self.height = height

    @classmethod
    def random(classs, width:float, height:float):  #generate random Field  (width, height im Bereich von 1000)
        food = {}
        obstacles = {}
        foodAmount = int(width*height / 100)
        obstacleAmount = int(width*height /100000)
        for i in range(foodAmount):
            randomBall = Ball.random(width, height, 5)
            food[i] = randomBall
        for i in range(obstacleAmount):
            randomObstacle = Ball.random(width, height, 40)
            obstacles[i] = randomObstacle
        return classs(food, obstacles, {}, width, height)

    def addPlayer(self, id:int, player:Player):
        self.players[id] = player



def testWorld(printing = False):
    player1 = testPlayer()
    player2 = testPlayer()
    playerDict = {1:player1, 2:player2}
    obstacle = testBall()
    food = testBall()

    myWorld = World({1:food}, {1:obstacle}, playerDict, 3, 4)
    if printing: print(myWorld.players[1].name , "== Max")
    if printing: print(World.random(2000, 1000).obstacles[0].position.x, "== random")

    World.random(2000, 1000)

    return myWorld


if __name__ == '__main__':
    testWorld(True)
