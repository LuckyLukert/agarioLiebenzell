import socketserver
import socket
import threading
from server1 import *

class ServerThread(threading.Thread):

    listening = True
    def listen(self):

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print("Binding to port 60001")
        s.bind(('localhost', 60001))

        s.listen()

        while True:
            (client, addr) = s.accept()

            threading.Thread(target=(self.listenClient), args=(client,)).start()
            # TODO Add client to list

    def listenClient(self, client):
        while True:
            data = ''
            while True:
                data += client.recv(2048).decode("utf-8")
                if "\n" in data:
                    break
            print("New data: " + data)
            client.send( bytearray("Agar IO Test: Recv " +data, "utf-8"))

            ## Fire event
            

    def send(self, client, data):
        client.send(data=data)


if __name__ == "__main__":
    ServerThread().listen()
