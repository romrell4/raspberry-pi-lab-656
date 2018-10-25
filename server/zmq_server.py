import importlib
import os
import subprocess

import zmq

import marionberry_handler

editor = os.environ.get('EDITOR','vim')

class ThreadedServer:
    def __init__(self, port):
        self.ip_address = "Erics-Macbook"
        self.port = port
        self.clients = []
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)

    def listen(self):
        socket = self.context.socket(zmq.REP)
        socket.bind("tcp://*:1234")

        while True:
            try:
                print("Listening for requests on port {}".format(self.port))
                json_request = socket.recv_json()
                response = self.handle_request(json_request)
                socket.send_json(response)
            except Exception as e:
                print("Error occurred: {}".format(e))
                socket.send_json({"status": "Failed"})

    def handle_request(self, json_request):
        if json_request.get("action") == "register":
            print("Registering new client: {}".format(json_request))
            client = Client(json_request)

            # open a tcp connection and send my address.
            return {"client_id": client.client_id}
        elif json_request.get("client_id") is not None:
            client_id = json_request["client_id"]
            client = next(iter([client for client in self.clients if client.client_id == client_id]))
            if client is not None:
                action = json_request.get("action")
                if action == "edit":
                    print("Handling edit request...")
                    subprocess.call([editor, "marionberry_handler.py"])
                    importlib.reload(marionberry_handler)
                    return {"status": "OK"}
                elif action == "act":
                    print("Handling act request...")
                    response = marionberry_handler.handle(self.clients)
                    if response is not None:
                        return response
                    else:
                        return {"error": "No response from handler code"}
                else:
                    print("Unknown action: '{}' sent from client: '{}'".format(action, client_id))
            else:
                print("Request from unknown client: {}".format(client_id))
        else:
            print("Unknown request: {}".format(json_request))

        # If we hit this line, we didn't process their request properly
        return {"status": "Failed"}

class Client:
    def __init__(self, json_data):
        self.client_id = len(server.clients) + 1
        self.hostname = json_data["hostname"]
        self.port = json_data["port"]
        self.socket = zmq.Context().socket(zmq.REQ)
        self.socket.connect("tcp://{}:{}".format(self.hostname, self.port))

        server.clients.append(self)

    def send(self, json_request):
        print("Sending to client {}: {}".format(self.client_id, json_request))
        self.socket.send_json(json_request)
        print("Received back: {}".format(self.socket.recv_json()))

    def led_on(self):
        self.send({"action": "led_on"})

    def led_off(self):
        self.send({"action": "led_off"})


if __name__ == "__main__":
    server = ThreadedServer(1234)
    server.listen()
