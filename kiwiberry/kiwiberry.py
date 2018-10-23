#!/usr/bin/python3

from threading import Thread
import utilities
import json
from gpiozero import LED

led = LED(17)

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
            if message == "light_on":
                led.on()
            elif message == "light_off":
                led.off()

    def send(self, message):
        utilities.send(message, self.server_ip_address, self.server_port)


pi = RaspberryPi("kiwiberry", 4321)

# import time
# while True:
#     led.on()
#     time.sleep(1)
#     led.off()
#     time.sleep(1)

Thread(target = pi.listen).start()
