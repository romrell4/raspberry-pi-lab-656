#!/usr/bin/python3

import zmq
from gpiozero import LED

led = LED(17)

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

    def listen(self):
        while True:
            print("Waiting for request...")
            request = self.socket.recv_json()
            print("Received: {}".format(request))
            if "action" in request:
                action = request["action"]
                if action == "led_on":
                    led.on()
                elif action == "led_off":
                    led.off()
            else:
                self.socket.send_json({"error": "No action in request"})


pi = RaspberryPi("kiwiberry", 4321)
pi.listen()
