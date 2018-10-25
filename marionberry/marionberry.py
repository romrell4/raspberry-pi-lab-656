#!/usr/bin/python3

import zmq
# from gpiozero import Button

class RaspberryPi:
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port
        self.socket = zmq.Context().socket(zmq.REQ)
        self.socket.connect("tcp://Erics-Macbook:1234")

        # Send a message to register with the server
        print("Connecting to server...")
        self.socket.send_json({"action": "register", "hostname": self.hostname, "port": self.port})
        response = self.socket.recv_json()
        if "client_id" not in response:
            print("Bad response from server: {}".format(response))
            exit(-1)
        print("Success!")
        self.client_id = response["client_id"]

    def send(self, action):
        self.socket.send_json({"client_id": self.client_id, "action": action})
        print("Response from server: {}".format(self.socket.recv_json()))


# edit_button = Button(3)
# act_button = Button(4)

pi = RaspberryPi("marionberry", 4321)

# edit_button.when_pressed = lambda: pi.send("edit")
# act_button.when_pressed = lambda: pi.send("act")

while True:
    command = input("Command: ")
    pi.send(command)
