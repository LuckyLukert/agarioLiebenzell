from json import JSONDecoder
import eventhandler

# TODO implement events in network
eventsExecute = {
    'wantToJoin': lambda event, world: ,
    'move': lambda event, world: 
}


def eventFromJSON(json):
    decode = JSONDecoder().decode(json)
    return Event(**decode)

class Event:
    def __init__(self, name, **entries):
        self.event = None
        self.__dict__.update(entries)


    def __init__(self, name):
        self.event = name

    def execute(self, world):
        eventsExecute[self.event](self, world)

