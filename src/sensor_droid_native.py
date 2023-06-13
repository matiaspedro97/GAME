from sensordroid import Client
import time


def devicesDiscoveredEventHandler(devices):
    print(devices)
    if len(devices) > 0:
        client = Client(devices[0])

        client.connectionUpdated = connectionUpdatedEventHandler
        client.sensorsReceived = sensorsReceivedEventHandler
        client.imageReceived = cameraReceivedEventHandler

        client.sensorsSampleRate = 50
        client.cameraResolution = 13

        client.connect()


def connectionUpdatedEventHandler(sender, msg):
    if sender is not None:
        if sender.connected:
            print("Connected")
        else:
            print("Disonnected")


def sensorsReceivedEventHandler(sender, dataCurrent):
    print(f"{sender.name}: Acceleration [{dataCurrent.Acceleration.Values.AsString}]")


def cameraReceivedEventHandler(sender, image):
    # Process image data bytes
    pass


if __name__ == '__main__':
    Client.devicesDiscovered = devicesDiscoveredEventHandler
    print(Client.connected)
    print(Client.sensorsReceived)
    Client.startDiscovery()

    key = input("Press ENTER to exit\n")

    Client.closeAll()
