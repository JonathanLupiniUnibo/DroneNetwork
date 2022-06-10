from socket import *
import sys

host = "localhost"
router_port = 12000
drone_port = 12001

clientsocket = socket(AF_INET, SOCK_DGRAM)
clientsocket.bind((host, drone_port))
serverAddressPort = (host, router_port)
while True:
    try:
        print ("Waiting for order")
        data, server = clientsocket.recvfrom(4096)
        print ('received message "%s"' % data.decode('utf8'))
        print(data.decode())
    except Exception as info:
        print(info)


