from json import JSONDecoder


def eventFromJSON(json):
    decode = JSONDecoder().decode(json)
    for key in decode:
        if key == "join":
            return JoinRequestEvent(decode[key])



class Event:
    def __init__(self):
        print("")

class JoinRequestEvent (Event):
    def __init__(self, json):
        self.name = json["name"]