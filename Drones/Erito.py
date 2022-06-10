from socket import *
import sys
import random
import time

host = "localhost"

router_port = 12000
router_ip = "192.168.1.0"
IpToPort = {
        router_ip : router_port
    }

drone_port = 12002
droneName = "Erito"

clientsocket = socket(AF_INET, SOCK_DGRAM)
clientsocket.bind((host, drone_port))
serverAddress = (host, router_port) # simula una connessione su un'interfaccia diversa dal loopback
while True:
    try:
        roundTrip = random.randint(4, 10)
        print ("Waiting for order")
        data, server = clientsocket.recvfrom(4096)
        if data.decode() == "END":
            break
        print ('received delivery address: "%s"' % data.decode('utf8'))
        print ("Delivering...")
        time.sleep(roundTrip/2)
        print ("Package Delivered! Returning to warehouse...")
        time.sleep(roundTrip/2)
        print ("Arrived to warehouse\n")
        message = droneName + " available"
        clientsocket.sendto(message.encode(), serverAddress)
    except Exception as info:
        print(info)

print("Drone shutting down")
clientsocket.close()
sys.exit(0)
