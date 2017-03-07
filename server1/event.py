from json import JSONDecoder
from json import JSONDecodeError
from json import JSONEncoder


import world

# TODO implement events in network
eventsExecute = {
    'wantToJoin': lambda event, game: {
        print("Client " + event.name + " wants to join")
        # Handle join

    },
    'move': lambda event, game: {
        print("Client " + event.sender + " moves " + str(event.direction))
    }
}


def eventFromJSON(json, senderId):
    try:
        decode = JSONDecoder().decode(json)
    except JSONDecodeError:
        print(str(senderId) + " sent malformed json: " + json)
        return None
    return Event(senderId, decode)


def eventToJSON(event):
    enc = event.__dict__.copy()
    enc.pop("sender")
    decode = JSONEncoder().encode(enc)
    return decode


class Event:
    def __init__(self, sender, entries):
        self.event = None
        self.sender = sender
        self.__dict__.update(entries)
        print("Sender " + str(sender))

    def execute(self, game):
        eventsExecute[self.event](self, game)

