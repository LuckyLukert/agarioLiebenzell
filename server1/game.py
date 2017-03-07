from multiprocessing import SimpleQueue
from event import *
from eventhandler import *
from world import *
from network import *
import time

class Game:
    def __init__(self):
        self.evHandler = EventHandler(self.clientEvt)
        self.world = World.random()
        self.eventQueue = SimpleQueue()
        self.evHandler.start()

    def iteratePlayerBalls(self):
        for playerId in self.world.players:
            player = self.world.players[playerId]
            for ballId in range(len(player.balls)):
                ball = player.balls[ballId]
                yield(player, playerId, ball, ballId)


    def eat(self):
        foodRemoveIds = []
        for foodId in self.world.food:
            food = self.world.food[foodId]
            nearestId = -1
            nearestBallId = -1
            minDist = 1000000000
            for (player, playerId, ball, ballId) in self.iteratePlayerBalls():
                dist = (food.position - ball.position).length()
                if (dist < ball.size and dist < minDist):
                    nearestId = playerId
                    nearestBallId = ballId
                    minDist = dist

            if nearestId != -1:
                self.world.players[nearestId].balls[nearestBallId].size += food.size
                foodRemoveIds.append(foodId)
                foodRemove = {"event":"foodRemove", "id":foodId}
                self.evHandler.broadcast(Event(foodRemove))
        for idd in foodRemoveIds:
            self.world.food.pop(idd)



    def attack(self):
        ballRemoveIds = []
        for (player1, playerId1, ball1, ballId1) in self.iteratePlayerBalls():
            for (player2, playerId2, ball2, ballId2) in self.iteratePlayerBalls():
                if (playerId1 != playerId2):  #unterschiedliche Spieler
                    dist = (ball1.position - ball2.position).length()
                    sizeDist = ball1.size - ball2.size
                    sizeSum = ball1.size + ball2.size
                    if dist < sizeSum*2:  #nah genug
                        if sizeDist > 20:  #ball1 größer
                            ball1.size += ball2.size
                            ballRemoveIds.append((playerId2, ballId2))
                        if sizeDist < -20:  #ball2 größer
                            ball2.size += ball1.size
                            ballRemoveIds.append((playerId1, ballId1))
        for (playerId, ballId) in ballRemoveIds:
            self.world.players[playerId].balls.pop(ballId)


    def step(self):
        moves = []

        #Spieler bewegen
        for idd in self.world.players:
            self.world.players[idd].move()

        #Spieler fressen
        self.eat()

        #Spieler attackieren einander
        self.attack()



        #Spieler move-Events senden
        for idd in self.world.players:
            player = self.world.players[idd]
            moves.append({"id":idd, "balls": player.balls})
        event = {
          "event": "playerMoves",
          "moves": moves
        }
        self.evHandler.broadcast(Event(event))


    def run(self):
        while True:
            self.step()
            while not self.eventQueue.empty():
                event = self.eventQueue.get()
                event.execute(self)
            time.sleep(0.1)


    def clientEvt(self, event:Event):
        self.eventQueue.put(event)



def testGame():
    game = Game()
    print("Successfully started Game")
    game.step()

if __name__ == '__main__':
    testGame()
