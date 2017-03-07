import socketserver
import socket
import threading
import eventhandler
from json import JSONEncoder

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

        print("Binding to port 60001")
        s.bind(('localhost', 60001))
        s.listen()
        while True:
            (client, addr) = s.accept()

            threading.Thread(target=(self.listenClient), args=(client,id,eventhandler)).start()
            self.clients[id] = client
            self.ids += 1

    def listenClient(self, client, id, eventhandler):
        while True:
            data = ''
            while True:
                data += client.recv(2048).decode("utf-8")
                if "\n" in data:
                    break
            print("New data: " + data)
            client.send( bytearray("Agar IO Test: Recv " +data, "utf-8"))

            # Fire event
            eventhandler.proceedData(data, id)

    def send(self, id, data):
        self.clients[id].send(data=data)

    def broadcast(self, data):
        for client in self.clients:
            client.send(data)



def callbackTest(event):
    print(JSONEncoder().encode(event.__dict__))

if __name__ == "__main__":
    st = ServerThread()
    ev = eventhandler.EventHandler(callbackTest, st)
    st.start(ev)

    # Test
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 60001))
    print("Sending to socket...")
    s.send("{\"test\":\"test\"}\n".encode("utf-8"))
