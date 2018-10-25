#!/usr/bin/python3

import zmq
from gpiozero import LED

led = LED(17)

class RaspberryPi:
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port

        # Send a message to register with the server
        print("Connecting to server...")
        socket = zmq.Context().socket(zmq.REQ)
        socket.connect("tcp://Erics-Macbook:1234")
        socket.send_json({"action": "register", "hostname": self.hostname, "port": self.port})
        response = socket.recv_json()
        if "client_id" not in response:
            print("Bad response from server: {}".format(response))
            exit(-1)
        print("Success!")
        self.client_id = response["client_id"]

    def listen(self):
        socket = zmq.Context().socket(zmq.REP)
        socket.bind("tcp://*:{}".format(self.port))

        while True:
            print("Waiting for request...")
            request = socket.recv_json()
            print("Received: {}".format(request))
            if "action" in request:
                action = request["action"]
                if action == "led_on":
                    print("Turning led on")
                    led.on()
                    socket.send_json({"status": "OK"})
                elif action == "led_off":
                    print("Turning led off")
                    led.off()
                    socket.send_json({"status": "OK"})
                else:
                    print("Unknown action")
                    socket.send_json({"error": "Unknown action: {}".format(action)})
            else:
                socket.send_json({"error": "No action in request"})


pi = RaspberryPi("kiwiberry", 4321)
pi.listen()
