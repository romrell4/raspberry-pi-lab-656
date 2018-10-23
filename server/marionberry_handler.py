def handle(clients):
    kiwiberry = next(iter([client for client in clients if client.name == "kiwiberry"]), None)
    if kiwiberry is not None:
        print("Turning on kiwiberry's light...")
        kiwiberry.led_on()
    else:
        print("Couldn't find kiwiberry")
