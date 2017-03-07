import socketserver
import socket
import threading
import eventhandler
from eventhandler import *
from json import JSONEncoder
from settings import *

class ServerThread:

    listening = True

    def __init__(self):
        self.clients = dict()
        self.ids = 0

    def start(self, eventhandler):
        threading.Thread(target=self.__listen, args=(eventhandler,)).start()

    # Start socket via .start()
    def __listen(self, eventhandler):

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print("Binding to port " + str(PORT))
        s.bind((socket.gethostname(), PORT))
        s.listen()
        while True:
            (client, addr) = s.accept()
            threading.Thread(target=(self.listenClient), args=(client,self.ids,eventhandler)).start()
            self.clients[self.ids] = client
            self.ids += 1

    def listenClient(self, client, id, eventhandler):
        while True:
            data = ''
            while True:
                try:
                    data += client.recv(2048).decode("utf-8")
                except UnicodeDecodeError:
                    continue
                except BaseException:
                    self.clients.pop(id)
                    return
                if "\n" in data:
                    break
            print("New data: " + data)
            #client.send( bytearray("Agar IO Test: Recv " +data, "utf-8"))

            # Fire event
            eventhandler.proceedData(data, id)

    def send(self, id, data):
        try:
            self.clients[id].send((data + "\n").encode("utf-8"))
        except BaseException:
            print("Tried to send to closed socket")
            return

    def broadcast(self, data):
        for client in self.clients:
            self.send(client, data)



def callbackTest(event):
    print("Ev to json" +eventToJSON(event))
    print("Native json: " + JSONEncoder().encode(event.__dict__))

if __name__ == "__main__":
    st = ServerThread()
    ev = eventhandler.EventHandler(callbackTest, st)
    st.start(ev)

    # Test
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', PORT))
    print("Sending to socket...")
    s.send("{\"event\":\"wantToJoin\", \"name\":\"Simon\"}\n".encode("utf-8"))
