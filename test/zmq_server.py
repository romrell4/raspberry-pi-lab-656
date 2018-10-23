import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:1111")

while True:
    print("Waiting for request...")
    message = socket.recv()
    print("Received message: {}".format(message.decode("utf-8")))

    socket.send("OK".encode("utf-8"))