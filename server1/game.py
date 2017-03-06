from multiprocessing import SimpleQueue
from event import *
from eventhandler import *

class Game:
    def __init__(self, evHandler:EventHandler):
        self.evHandler = evHandler

    def init(self):
        self.world = testWorld()
        self.eventQueue = SimpleQueue()

    def step(self):
        moves = []
        for player in self.world.players:
            player.move()
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
