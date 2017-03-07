from multiprocessing import SimpleQueue
from event import *
from eventhandler import *

class Game:
    def __init__(self, evHandler:EventHandler):
        self.evHandler = evHandler
        self.world = World.random()
        self.eventQueue = SimpleQueue()

    def step(self):
        moves = []

        #Spieler bewegen
        for idd in self.world.players:
            self.world.players[idd].move()

        #Spieler fressen
        for foodId in self.world.food:
            food = self.world.food[foodId]
            nearestId = -1
            nearestBallId = -1
            minDist = 1000000000
            for playerId in self.world.players:
                player = self.world.players[playerId]
                for ballId in player.balls:
                    ball = player.balls[ballId]
                    dist = len(food.position - ball.position)
                    if (dist < ball.size and dist < minDist):
                        nearestId = playerId
                        nearestBallId = ballId
                        minDist = dist
            if nearestId != -1:
                self.world.players[nearestId].balls[nearestBallId].size += food.size
                self.world.food.pop(foodId)
                foodRemove = {"event":"foodRemove", "id":foodId}
                evHandler.sendfoodRemove = Event(**foodRemove)


        #Spieler move-Events senden
        for idd in self.world.players:
            player = self.world.players[idd]
            moves.append({"id":player.id, "balls": player.balls})
        event = {
          "event": "playerMoves",
          "moves": moves
        }
        evHandler.send(Event(**event))


    def run(self):
        while True:
            step()
            while not self.eventQueue.empty():
                event = self.eventQueue.get()
                event.execute(self.world)


    def clientEvt(self, event:Event):
        eventQueue.put(event)
