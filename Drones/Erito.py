from socket import *
import sys

host = "localhost"
router_port = 12000
drone_port = 12001

clientsocket = socket(AF_INET, SOCK_DGRAM)
clientsocket.bind((host, drone_port))
serverAddressPort = (host, router_port)
message = "Erito "+ "available"    
while True:
    a = input("Send: ")
    print(message)
    clientsocket.sendto(str.encode(message), serverAddressPort)

