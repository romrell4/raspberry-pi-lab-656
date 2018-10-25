import zmq
import json

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:1234")

while True:
    print("Waiting for request...")
    message = socket.recv_json()
    print("Received message: {}\nSending message...".format(message))
    socket.send_json({"status": "OK"})