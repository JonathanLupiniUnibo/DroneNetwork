from socket import *
import sys

#TODO wrapper per indirizzi IP

clientsocket = socket(AF_INET, SOCK_STREAM)

host = "localhost"
port = 10000

DroneToIp = {
    "Etalide" : "192.168.1.1",
    "Erito" : "192.168.1.2",
    "Eudoro" : "192.168.1.3"
    }

drone = input("Name of the drone: ")
address = input("Shipping address: ")
message = drone+" "+address
try:
    clientsocket.connect((host,port))
except Exception as data:
    print (Exception,":",data)
    print ("Ritenta sarai più fortunato.\r\n")
    sys.exit(0)  

if len(message.split())<2:
    print("Wrong input format")  
    clientsocket.close()
    quit()
if DroneToIp.__contains__(message.split()[0]):
    clientsocket.send(message.encode()) 
    response = clientsocket.recv(1024)
    print (response.decode())
else:
    print ("No such drone exists")
clientsocket.close()