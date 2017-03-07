from json import JSONDecoder
from json import JSONDecodeError
import world

# TODO implement events in network
eventsExecute = {
    'wantToJoin': lambda event, world: {

    },
    'move': lambda event, world: {

    }
}


def eventFromJSON(json, senderId):
    try:
        decode = JSONDecoder().decode(json)
    except JSONDecodeError:
        print(str(senderId) + " sent malformed json: " + json)
        return None
    return Event(senderId, decode)

class Event:
    def __init__(self, sender, entries):
        self.event = None
        self.__dict__.update(entries)


    def execute(self, world):
        eventsExecute[self.event](self, world)

