import socket

UDP_PORT = 1111

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address = s.getsockname()[0]
    s.close()
    return ip_address

def broadcast(message):
    print("Sending UDP broadcast: {}".format(message))
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(message.encode('utf-8'), ('255.255.255.255', UDP_PORT))
    sock.close()

def send(message, ip_address, port):
    print("Sending TCP message to {}:{}: {}".format(ip_address, port, message))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip_address, port))
    s.send(message.encode("utf-8"))
    s.close()

def receive(port):
    print("Listening for TCP messages on port {}".format(port))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(('', port))
    except OSError:
        pass
    s.listen(1)
    client, (client_ip_address, client_port) = s.accept()
    client.settimeout(60)
    print("Connection from {}".format(client_ip_address))
    message = ""
    while True:
        try:
            data = client.recv(512)
            if data:
                message = message + data.decode("utf-8")
            else:
                client.close()
                s.close()
                break
        except Exception as e:
            print("An error occurred: {}".format(e))
            client.close()
            s.close()
            break
    print("Received from {}:{}: {}".format(client_ip_address, client_port, message))
    return message, client_ip_address
