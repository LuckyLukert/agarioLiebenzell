from network import ServerThread
from event import eventFromJSON
from event import eventToJSON


class EventHandler:
    def __init__(self, callback, network: ServerThread):
        self.callback = callback
        self.network = network

    def proceedData(self, data, sender):
        event = eventFromJSON(data, sender)
        if event is None: return
        # callback should execute events synchronously
        self.callback(event)

    def broadcast(self, event):
        # TODO send data via network
        self.network.broadcast(eventToJSON(event))

    def send(self, event, id):
        self.network.send(id, eventToJSON(event))