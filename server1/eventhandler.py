from network import ServerThread
from event import eventFromJSON

class EventHandler:
    def __init__(self, callback, network: ServerThread):
        self.callback = callback
        self.network = network

    def proceedData(self, data):
        event = eventFromJSON(data)
        self.callback(*event)

    def send(self, event):
        # TODO send data via network
        self.network.send()

    def send(self, event, id):
        print("")