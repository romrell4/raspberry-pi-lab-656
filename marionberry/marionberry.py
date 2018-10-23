#!/usr/bin/python3

from threading import Thread
import utilities
import json
# from gpiozero import Button

class RaspberryPi:
    def __init__(self, name, tcp_port):
        self.name = name
        self.ip = utilities.get_ip_address()
        self.tcp_port = tcp_port
        self.server_ip_address, self.server_port = self.find_server()

    def as_json(self):
        return json.dumps({
            "name": self.name,
            "ip_address": self.ip,
            "port": self.tcp_port
        })

    def find_server(self):
        # Broadcast a message to find the server
        utilities.broadcast(self.as_json())

        # Wait for a tcp connection from the server
        response = json.loads(utilities.receive(self.tcp_port)[0])
        return response["ip_address"], response["port"]

    def listen(self):
        while True:
            message, _ = utilities.receive(self.tcp_port)

    def send(self, message):
        utilities.send(message, self.server_ip_address, self.server_port)


# edit_button = Button(3)
# act_button = Button(4)

pi = RaspberryPi("marionberry", 4321)

# edit_button.when_pressed = lambda: pi.send("edit")
# act_button.when_pressed = lambda: pi.send("act")

Thread(target = pi.listen).start()

while True:
    command = input("Command: ")
    pi.send(command)
