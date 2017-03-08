from json import JSONDecoder
from json import JSONDecodeError
from json import JSONEncoder
from player import *
from settings import *
from ball import Vector

# TODO implement events in network

def wantToJoinEvent(event, game):
    try:
        print("Client " + event.name + " wants to join")
        player = Player.random(str(event.name), WIDTH, HEIGHT)
        game.world.addPlayer(event.sender, player)
        ev1 = Event({"event":"join", "id":event.sender,"world":game.world})

        game.evHandler.send(ev1, event.sender)

    except AttributeError:
        print("ERR: Client " + str(event.sender) + " sent no name")
        pass

def wantToMove(event, game):
    #print("Updated speed of " + str(event.sender))
    for ball in game.world.players[event.sender].balls:
        ball.speed = Vector.byJSON(event.direction)

def disconnectClient(event, game):
    game.world.players.pop(event.sender)
    game.evHandler.network.clients.pop(event.sender)

def splitEvent(event, game):
    player = game.world.players[event.sender]
    player.split()



eventsExecute = {
    'wantToJoin': wantToJoinEvent,
    'move': wantToMove,
    'split': splitEvent,
    'disconnect': disconnectClient,
    'wantToWatch': lambda event, game: {
        print("Client " + str(event.sender) + " joins as watcher!")
    },
    'shoot': lambda event, game: {
        print("Client " + str(event.sender) + " shoots!")
    }
    # Add events

}




class Event:
    def __init__(self, entries, sender=None):
        self.event = None
        self.sender = sender
        self.__dict__.update(entries)
    #    print("Event created [name=" + str(self.event) + "; sender=" + str(sender) + "]")

    def execute(self, game):
        try:
            eventsExecute[self.event](self, game)
        except KeyError:
            pass

    def reprJSON(self):
        enc = self.__dict__.copy()
        enc.pop("sender")
        return enc
