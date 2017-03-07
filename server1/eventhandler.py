from network import ServerThread
from event import Event
import json

class EventHandler:
    def __init__(self, callback):
        self.callback = callback
        self.network = ServerThread()

    def start(self):
        self.network.start(self)

    def proceedData(self, data, sender):
        event = eventFromJSON(data, sender)
        print("Received Event: " + str(event))
        if event is None: return
        # callback should execute events synchronously
     #   print("Executing callback")
        self.queueEvent(event)

    def queueEvent(self, event):
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



def eventFromJSON(jsonstr, senderId):
    try:
        decode = json.JSONDecoder().decode(jsonstr)
    except json.JSONDecodeError:
        print(str(senderId) + " sent malformed json: " + jsonstr)
        return None
    return Event(decode, senderId)


def eventToJSON(event):
    decode = json.dumps(event.reprJSON(), cls=ComplexEncoder)
    return decode