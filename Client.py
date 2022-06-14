from socket import *
import sys
import threading
import os
import time

#TODO wrapper per indirizzi IP

endFlag = False
allConnected = False

def clear():
    print("\n" * 50)
    
def handle_send ():
    global endFlag
    global allConnected
    while True:
        time.sleep(1) # serve a dare il tempo al router di mandare la lista aggiornata di droni disponibili
        if endFlag == True:
            return        
        timeBegin = time.time()
        for device in DroneStatus:
            if DroneStatus[device] is None:
                break
            allConnected = True
            clear()
        if allConnected == False:
            clear()
            print("Not all drones are connected")
            continue
        for device in DroneStatus:
            print(device+" is",end = ' ')
            if DroneStatus[device] == "available":
                print("available")
            else:
                print("unavailable")        
        drone = input("Name of the drone: ")
        if drone == "END":
            message = "END"
            clientsocket.send(message.encode())
            endFlag = True
            return
        elif drone == "update":
            clear()
            continue
        address = input("Shipping address: ")
        message = client_ip+" "+drone+" "+address
        if time.time() - timeBegin >= 20:
            clear()
            print("Too much time has passed, new Drones might be available")
            print("")
            continue
        if len(message.split())<2:
            clear()
            print("Wrong input format")
        elif DroneStatus.__contains__(drone):
            if DroneStatus[drone] == "available":
                clientsocket.send(message.encode())
                clear()
            else:
                clear()
                print(drone+" is currently busy\r\n")
        else:
            clear()
            print ("No such drone exists\r\n")

def handle_receive():
    global endFlag
    while True:
        if endFlag == True:
            return
        try:
            response = clientsocket.recv(1024)
            response = response.decode("utf-8");
            if response == "Ending started":
                endFlag = True
                return
            i = 1;
            limit = len(response.split())/3
            while i <= limit:
                target = response.split()[3*(i-1)]
                status = response.split()[i*3-1]
                DroneStatus[target] = status
                i += 1
        except Exception as error:
            print (Exception,":",error)
            print ("Something went wrong\r\n")
            endFlag = True
            return
            
host = "localhost"

router_port = 10000
router_ip =  "10.10.10.01"

client_port = 8000
client_ip = "10.10.10.0"

clientsocket = socket(AF_INET, SOCK_STREAM)
clientsocket.bind((host, client_port))


RouterPort = {
        "10.10.10.01" : router_port
    }

DroneStatus = {
    "Etalide" : None,
    "Erito" : None,
    "Eudoro" : None
    }

try:
    clientsocket.connect((host,RouterPort[router_ip]))
except Exception as data:
    print (Exception,":",data)
    print ("Something went wrong when connecting to the router \r\n")
    clientsocket.close()
    sys.exit(0)   

send_thread = threading.Thread(target=handle_send)
send_thread.start()
receive_thread = threading.Thread(target=handle_receive)
receive_thread.start()
while True:
    time.sleep(1)
    if endFlag == True:
        break
time.sleep(2)    
clientsocket.close()
clear()
print("Client shutdown")



        