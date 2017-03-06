from server1.event import *


class EventHandler:
    def __init__(self, callback):
        self.callback = callback

    def proceedData(self, data):
        event = eventFromJSON(data)
        self.callback(*event)

    def send(self, event):
        print("")

    def send(self, event, id):
        print("")