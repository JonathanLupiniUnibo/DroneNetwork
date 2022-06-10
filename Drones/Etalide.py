from socket import *
import sys

clientsocket = socket(AF_INET, SOCK_DGRAM)

host = "localhost"
port = 12000
serverAddressPort =(host, port)
message = "Etalide "+ "True"    
print(message)
clientsocket.sendto(str.encode(message), serverAddressPort)

