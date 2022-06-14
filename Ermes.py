from socket import *
import threading
import time
import sys

#netstat -ano|findstr 10000

endFlag = False
allConnected = False


def shutDown():
    global endFlag
    print("Router shutting down")
    for drone in DroneToIp:
        message = "END"
        address = (host, IpToPort[DroneToIp[drone]])
        router_drone_socket.sendto(message.encode("utf-8"), address)
    endFlag = True
    time.sleep(2) #giving time to the threads to finish their business
    router_client_socket.close()
    router_drone_socket.close()
    print("Router shutdown")  # client_update_thread si aggiorna ogni 0.1 secondi, non c'è bisogno di chiuderlo
    sys.exit(0)
    

def updateClient():
    global endFlag
    global client_ip
    global allConnected
    while allConnected == False:
        time.sleep(1)
    print("Client is now available\n")
    message = ""
    for drone in DroneStatus:
        message = message + drone+ " is " + DroneStatus[drone]+ " "
    connectionSocket.send(message.encode())    
    while True:
        if endFlag == True:
            return
        if client_ip is None: #parte solo quando è stato fatto almeno un ordine
            continue
        time.sleep(0.1)
        message = ""
        # print("Router["+client_facing_ip+"] tells Client["+client_ip+"] that : \n") # comment out for clarity when reading the router console
        for drone in DroneStatus:
            message = message + drone+ " is " + DroneStatus[drone]+ " "
        connectionSocket.send(message.encode())
        # print(message+"\n") # comment out for clarity when reading the router console                
                
def handleClient():           
    global endFlag
    global client_ip
    while True:
        if endFlag == True:
            return
        try:
            message = connectionSocket.recv(1024)
            message = message.decode()
            if message == "END":
                answer = "Ending started"
                connectionSocket.send(answer.encode())
                shutDown()
                return
            drone = message.split()[1]
            if drone in DroneStatus:
                DroneStatus[drone] = "unavailable";
                ip = message.split()[0]
                if client_ip is None:
                    client_ip = ip
                shippingAddress = ' '.join(message.split()[2:])
                port = IpToPort[DroneToIp[drone]]
                target = ("localhost", port)
                print("Client["+ ip+"] wants "+drone+"["+DroneToIp[drone]+"] to deliver to "+ shippingAddress)
                router_drone_socket.sendto(shippingAddress.encode(), target)
        except Exception as error:
            if endFlag == True:
                return
            print (Exception,":",error)
            print ("Something went wrong when talking to the client\r\n")
            shutDown()
            return
            
def droneListen():
    global endFlag
    global allConnected
    
    while allConnected == False:
        print("\n" * 50)
        print("Waiting for all drones to connect")
        message, droneAddress = router_drone_socket.recvfrom(1024)
        message = message.decode("utf-8")
        if message in DroneStatus:
            DroneStatus[message] = "available"
            allConnected = True
            for device in DroneStatus:
                if DroneStatus[device] is None:
                    allConnected = False
        print("All drones connected\n")            
    while True:
        if endFlag == True:
            return
        try:
            message, droneAdress = router_drone_socket.recvfrom(1024)
            message = message.decode("utf-8")
            ip = message.split()[0]
            drone = message.split()[1]
            status = message.split()[2]
            print(drone+"["+ip+"] reports to Router["+drone_facing_ip+"] that it completed the delivery\n")
            DroneStatus[drone] = status;
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

client_ip = None #aspettiamo la prima interazione col client per scoprire l'ip

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
        "192.168.1.3": 12003,
    }

DroneStatus = {
    "Etalide" : None,
    "Erito" : None,
    "Eudoro" : None
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






