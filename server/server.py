import socket
from threading import Thread
import utilities
import json
import os
import subprocess
import marionberry_handler
import importlib

editor = os.environ.get('EDITOR','vim')

class ThreadedServer:
    def __init__(self, tcp_port):
        self.ip_address = utilities.get_ip_address()
        self.tcp_port = tcp_port
        self.clients = []

        # starting up a separate thread to listen for broadcasts from new berries.
        Thread(target = self.listen_for_new_clients).start()
        Thread(target = self.listen_for_messages).start()

    def as_json(self):
        return json.dumps({"ip_address": self.ip_address, "port": self.tcp_port})

    def listen_for_new_clients(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(('', utilities.UDP_PORT))

        print("Listening for UDP broadcasts on port {}".format(utilities.UDP_PORT))
        while True:
            data = s.recv(256)
            message = data.decode("utf-8")
            print("Received UDP broadcast: {}".format(message))
            Thread(target = self.handle_new_client, args = (data,)).start()

    def handle_new_client(self, data):
        client = Client(data)
        self.clients.insert(0, client)

        # open a tcp connection and send my address.
        utilities.send(self.as_json(), client.ip_address, client.port)

    def listen_for_messages(self):
        while True:
            message, sender = utilities.receive(self.tcp_port)
            Thread(target = self.handle_new_message, args = (message, sender)).start()

    def handle_new_message(self, message, sender):
        client = next(iter([client for client in self.clients if client.ip_address == sender]))
        if client is not None:
            if message == "edit":
                filename = "{}_handler.py".format(client.name)
                subprocess.call([editor, filename])
                importlib.reload(marionberry_handler)
            elif message == "act":
                marionberry_handler.handle(self.clients)
        else:
            print("Request from unknown sender: {}".format(sender))

    def send(self, message, client):
        utilities.send(message, client.ip_address, client.port)


class Client:
    def __init__(self, tcp_data):
        json_data = json.loads(tcp_data.decode("utf-8"))
        self.name = json_data["name"]
        self.ip_address = json_data["ip_address"]
        self.port = json_data["port"]

    def led_on(self):
        utilities.send("led_on", self.ip_address, self.port)


if __name__ == "__main__":
    ThreadedServer(1234)
