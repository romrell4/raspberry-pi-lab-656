def handle(clients):
    kiwiberry = next(iter([client for client in clients if client.hostname == "kiwiberry"]), None)
    if kiwiberry is not None:
        print("Turning on kiwiberry's light...")
        kiwiberry.led_off()
        return {"status": "OK"}
    else:
        print("Couldn't find kiwiberry")
        return {"error": "Couldn't find kiwiberry"}
