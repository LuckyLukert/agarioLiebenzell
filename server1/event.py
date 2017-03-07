from json import JSONDecoder
from json import JSONDecodeError
from json import JSONEncoder


# TODO implement events in network
eventsExecute = {
    'wantToJoin': lambda event, game: {
        print("Client " + event.name + " wants to join")
        # Handle join

    },
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
    def __init__(self, sender, entries):
        self.event = None
        self.sender = sender
        self.__dict__.update(entries)
        print("Sender " + str(sender))

    def execute(self, game):
        eventsExecute[self.event](self, game)

    def reprJSON(self):
        enc = __dict__.copy()
        enc.pop("sender")
        return enc
