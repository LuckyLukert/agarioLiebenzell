from network import ServerThread
from event import Event
import json

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


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj,'reprJSON'):
            return obj.reprJSON()
        else:
            return json.JSONEncoder.default(self, obj)



def eventFromJSON(json, senderId):
    try:
        decode = json.JSONDecoder().decode(json)
    except json.JSONDecodeError:
        print(str(senderId) + " sent malformed json: " + json)
        return None
    return Event(senderId, decode)


def eventToJSON(event):
    decode = json.dumps(event.reprJSON(), cls=ComplexEncoder)
    return decode