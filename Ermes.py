from socket import *
import threading
import time
import sys

#netstat -ano|findstr 10000

endFlag = False

def shutDown():
    global endFlag
    print("Router shutting down")
    for drone in DroneToIp:
        message = "END"
        address = (host, IpToPort[DroneToIp[drone]])
        router_drone_socket.sendto(message.encode("utf-8"), address)
    endFlag = True
    time.sleep(1) #giving time to the threads to finish their business
    router_client_socket.close()
    router_drone_socket.close()
    print("Router shutdown")  # client_update_thread si aggiorna ogni 0.1 secondi, non c'è bisogno di chiuderlo
    sys.exit(0)
    

def updateClient():
    global endFlag
    while True:
        if endFlag == True:
            return
        time.sleep(0.1)
        message = ""
        for drone in DroneStatus:
            message = message + drone 
            if DroneStatus[drone] == "available":
                message = message+" is available "
            else:
                message = message+" is unavailable "
        connectionSocket.send(message.encode())                
                
def handleClient():           
    global endFlag
    while True:
        if endFlag == True:
            return
        print ('Waiting for order')
        try:
            message = connectionSocket.recv(1024)
            message = message.decode()
            if message == "END":
                answer = "Ending started"
                connectionSocket.send(answer.encode())
                shutDown()
                return
            drone = message.split()[0]
            if drone in DroneStatus:
                DroneStatus[drone] = not DroneStatus[drone];
                address = message.split(' ', 2)[1]
                port = IpToPort[DroneToIp[drone]]
                target = ("localhost", port)
                router_drone_socket.sendto(address.encode(), target)
        except Exception as error:
            if endFlag == True:
                return
            print (Exception,":",error)
            print ("Something went wrong when talking to the client\r\n")
            shutDown()
            return
            
def droneListen():
    global endFlag
    while True:
        if endFlag == True:
            return
        print ("Listening to drones")
        try:
            message, droneAdress = router_drone_socket.recvfrom(1024)
            message = message.decode("utf-8")
            print("Drone said : "+message)
            drone = message.split()[0]
            status = message.split()[1]
            DroneStatus[drone] = status;
            print(DroneStatus[drone])
        except Exception as error:
           if endFlag == True:
                return
           print (Exception,":",error)
           print ("Something went wrong when listening to drone\r\n")    
           shutDown()
           return
             

host = "Localhost"

client_facing_port = 10000
drone_facing_port = 12000

client_facing_ip = "10.10.10.01"
drone_facing_ip = "192.168.1.0"

router_client_socket = socket(AF_INET, SOCK_STREAM)      # socket per il collegamento client-router
router_client_socket.bind((host, client_facing_port))

router_drone_socket = socket(AF_INET, SOCK_DGRAM)      # socket per il collegamento router-droni
router_drone_socket.bind((host, drone_facing_port))

DroneToIp = {
    "Etalide" : "192.168.1.1",
    "Erito" : "192.168.1.2",
    "Eudoro" : "192.168.1.3"
    }

IpToPort = {
        "192.168.1.1": 12001,
        "192.168.1.2": 12002,
        "192.168.1.3": 12003
    }

DroneStatus = {
    "Etalide" : "available",
    "Erito" : "available",
    "Eudoro" : "available"
    }
   

print ('the router is facing the client on port:',client_facing_port)
print ('the router is facing the drones on port:',drone_facing_port)

drone_listen_thread = threading.Thread(target=droneListen)
drone_listen_thread.start()

router_client_socket.listen(0)
connectionSocket, addr = router_client_socket.accept()

client_thread = threading.Thread(target = handleClient)
client_thread.start();
client_update_thread = threading.Thread(target = updateClient())
client_update_thread.start()






