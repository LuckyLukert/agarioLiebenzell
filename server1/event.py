from json import JSONDecoder
from json import JSONDecodeError
from json import JSONEncoder


# TODO implement events in network

def wantToJoinEvent(event, game):
    try:
        print("Client " + event.name + " wants to join")
        ev1 = Event({"event":"join", "id":event.sender,"world":game.world})
        game.evHandler.send(ev1, event.sender)
    except AttributeError:
        print("ERR: Client " + str(event.sender) + " sent no name")
        pass
eventsExecute = {
    'wantToJoin': wantToJoinEvent,
    'move': lambda event, game: {
        print("Client " + event.sender + " moves " + str(event.direction))
    },
    'wantToWatch': lambda event, game: {
        print("Client " + event.sender + " joins as watcher!")
    },
    'shoot': lambda event, game: {
        print("Client " + event.sender + " shoots!")
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
        eventsExecute[self.event](self, game)

    def reprJSON(self):
        enc = self.__dict__.copy()
        enc.pop("sender")
        return enc
