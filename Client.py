from socket import *
import sys
import threading
import os

#TODO wrapper per indirizzi IP

def clear():
    print("\n" * 50)
    
def handle_send (socket, ipList, status):
    while True:
        for device in status:
            print(device+" is",end = ' ')
            if status[device] == True:
                print("available")
            else:
                print("unavailable")        
        drone = input("Name of the drone: ")
        address = input("Shipping address: ")
        message = drone+" "+address
        if len(message.split())<2:
            clear()
            print("Wrong input format")  
        elif ipList.__contains__(drone):
            if status[drone] == True:
                socket.send(message.encode())
                clear()
            else:
                clear()
                print(drone+" is currently busy\r\n")
        else:
            clear()
            print ("No such drone exists\r\n")

def handle_recieve(socket, dictionary):
    while True:
        try:
            response = socket.recv(1024)
            response = response.decode("utf-8");
            i = 1;
            limit = len(response.split())/3
            while i <= limit:
                dictionary[response.split()[3*(i-1)]] = response.split()[i*3-1]
                i += 1
        except Exception as error:
            print (Exception,":",error)
            print ("Something went wrong\r\n")
            
host = "localhost"
router_port = 10000
client_port = 8000

clientsocket = socket(AF_INET, SOCK_STREAM)
clientsocket.bind((host, client_port))


DroneToIp = {
    "Etalide" : "192.168.1.1",
    "Erito" : "192.168.1.2",
    "Eudoro" : "192.168.1.3"
    }

DroneStatus = {
    "Etalide" : True,
    "Erito" : True,
    "Eudoro" : True
    }

try:
    clientsocket.connect((host,router_port))
except Exception as data:
    print (Exception,":",data)
    print ("Ritenta sarai più fortunato.\r\n")
    sys.exit(0)  

send_thread = threading.Thread(target=handle_send, args=(clientsocket, DroneToIp, DroneStatus))
send_thread.start()
recieve_thread = threading.Thread(target=handle_recieve(clientsocket, DroneStatus))
recieve_thread.start()
# while True:
#     try:
#         response = clientsocket.recv(1024)
#         response = response.decode("utf-8");
#         i = 1;
#         limit = len(response.split())/3
#         while i <= limit:
#             DroneStatus[response.split()[3*(i-1)]] = response.split()[i*3-1]
#             i += 1
#     except Exception as error:
#         print (Exception,":",error)
#         print ("Something went wrong\r\n")



        