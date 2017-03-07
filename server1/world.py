from player import *
from ball import *
from settings import *


class World:
    def __init__(self, food:{int:Ball}, obstacles:{int:Ball}, players:{int:Player}, width:float, height:float):
        self.food = food
        self.obstacles = obstacles
        self.players = players
        self.width = width
        self.height = height

    @classmethod
    def random(classs, width:float=WIDTH, height:float=HEIGHT):  #generate random Field  (width, height im Bereich von 1000)
        food = {}
        obstacles = {}
        foodAmount = int(width*height / 100)
        obstacleAmount = int(width*height /100000)
        for i in range(foodAmount):
            randomBall = Ball.random(width, height, FOOD_SIZE)
            food[i] = randomBall
        for i in range(obstacleAmount):
            randomObstacle = Ball.random(width, height, OBSTACLE_SIZE)
            obstacles[i] = randomObstacle
        return classs(food, obstacles, {}, width, height)

    def addPlayer(self, id:int, player:Player):
        self.players[id] = player

    def reprJSON(self):
        return self.__dict__.copy()


def testWorld(printing = False):
    player1 = testPlayer()
    player2 = testPlayer()
    playerDict = {1:player1, 2:player2}
    obstacle = testBall()
    food = testBall()

    myWorld = World({1:food}, {1:obstacle}, playerDict, 3, 4)
    if printing: print(myWorld.players[1].name , "== Max")
    if printing: print(World.random(2000, 1000).obstacles[0].position.x, "== random")

    return myWorld




if __name__ == '__main__':
    testWorld(True)
