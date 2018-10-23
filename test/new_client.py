import socket
import json

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address = s.getsockname()[0]
    s.close()
    return ip_address


print("Sending UDP")
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
udp_socket.sendto(json.dumps({"name": "marionberry", "ip_address": get_ip_address(), "port": 12345}).encode('utf-8'), ('255.255.255.255', 1111))
udp_socket.close()

tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.bind(("", 12345))
tcp_socket.listen(1)
client, _ = tcp_socket.accept()
client.settimeout(60)
message = ""
print("Waiting for response...")
while True:
    data = client.recv(512)
    if data:
        message += data.decode("utf-8")
    else:
        client.close()
        tcp_socket.close()
        break
print("Received: {}".format(message))
server = json.loads(message)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.connect((server["ip_address"], server["port"]))

while True:
    command = input("Command: ")
    server_socket.send(command.encode("utf-8"))
