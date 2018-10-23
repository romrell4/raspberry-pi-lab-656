import socket
import json

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address = s.getsockname()[0]
    s.close()
    return ip_address


udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind(('', 1111))

print("Waiting for broadcast...")
data = udp_socket.recv(256)
client = json.loads(data.decode("utf-8"))
print("Received: {}".format(client))
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((client["ip_address"], client["port"]))
client_socket.send(json.dumps({"ip_address": get_ip_address(), "port": 1234}).encode("utf-8"))
client_socket.close()

while True:
    print("Waiting for command...")
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind(('', 1234))
    tcp_socket.listen(1)
    client, _ = tcp_socket.accept()
    client.settimeout(60)
    message = ""
    while True:
        print("Receiving...")
        data = client.recv(256)
        if data:
            message += data.decode("utf-8")
        else:
            client.close()
            tcp_socket.close()
            break
    print("Received: {}".format(message))
