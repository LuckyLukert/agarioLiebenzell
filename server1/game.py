from multiprocessing import SimpleQueue
from event import *
from eventhandler import *
from world import *
from network import *
import time

class Game:
    def __init__(self):
        self.evHandler = EventHandler(self.clientEvt)
        self.world = testWorld()
        self.eventQueue = SimpleQueue()
        self.evHandler.start()

    def step(self):
        moves = []

        #Spieler bewegen
        for idd in self.world.players:
            self.world.players[idd].move()

        #Spieler fressen
        foodRemoveIds = []
        for foodId in self.world.food:
            food = self.world.food[foodId]
            nearestId = -1
            nearestBallId = -1
            minDist = 1000000000
            for playerId in self.world.players:
                player = self.world.players[playerId]
                for ballId in range(len(player.balls)):
                   # print(player.balls)
                    ball = player.balls[ballId]
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

        #Spieler move-Events senden
        for idd in self.world.players:
            player = self.world.players[idd]
            moves.append({"id":player.id, "balls": player.balls})
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
            time.sleep(5)


    def clientEvt(self, event:Event):
        self.eventQueue.put(event)
