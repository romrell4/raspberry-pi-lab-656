import zmq

socket = zmq.Context().socket(zmq.REQ)

print("Connecting to server...")
socket.connect("tcp://Erics-Macbook:1234")

print("Sending request...")
socket.send_json({"action": "register", "hostname": "kiwiberry", "port": 1234})
print(socket.recv_json())