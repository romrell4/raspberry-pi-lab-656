import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)

print("Connecting to server...")
socket.connect("tcp://Erics-Macbook:1111")

print("Sending request...")
socket.send("Hello World".encode("utf-8"))

print("Waiting for response...")
message = socket.recv()
print("Received: {}".format(message.decode("utf-8")))