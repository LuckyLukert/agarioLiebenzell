from json import JSONDecoder
from server1 import *

eventsExecute = {
    "join": lambda world: pass,



}


def eventFromJSON(json):
    decode = JSONDecoder().decode(json)
    for key in decode:
        return Event(key, **decode[key])

class Event:
    def __init__(self, name, **entries):
        self.event = name
        self.__dict__.update(entries)

    def __init__(self, name):
        self.eventName = name

    def execute(self, world):

