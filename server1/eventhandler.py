from network import ServerThread
from event import eventFromJSON


class EventHandler:
    def __init__(self, callback, network: ServerThread):
        self.callback = callback
        self.network = network

    def proceedData(self, data, sender):
        event = eventFromJSON(data, sender)
        if event is None: return
        self.callback(event)

    def broadcast(self, event):
        # TODO send data via network
        self.network.send()

    def send(self, event, id):
        print("")