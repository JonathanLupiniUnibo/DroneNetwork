from socket import *
import threading
import time

host = "Localhost"
client_facing_port = 10000
drone_facing_port = 12000
router_client_socket = socket(AF_INET, SOCK_STREAM)
router_client_socket.bind((host, client_facing_port))
router_drone_socket = socket(AF_INET, SOCK_DGRAM)
router_drone_socket.bind((host, drone_facing_port))

DroneToIp = {
    "Etalide" : "192.168.1.1",
    "Erito" : "192.168.1.2",
    "Eudoro" : "192.168.1.3"
    }

IpToPort = {
        "192.168.1.1": 12001,
        "192.168.1.2": 12002,
        "192.168.1.3": 120003
    }

DroneStatus = {
    "Etalide" : True,
    "Erito" : True,
    "Eudoro" : True
    }

print ('the router is up on port:',client_facing_port)

router_client_socket.listen(0);

connectionSocket, addr = router_client_socket.accept()
print(connectionSocket)
print(addr)

while True:

    print ('Ready to serve...')
    try:

        message = connectionSocket.recv(1024) ## riceve il messaggio di richiesta dal client
        drone = message.decode().split()[0]
        if drone in DroneStatus:
            DroneStatus[drone] = not DroneStatus[drone];
            answer = drone + " is "  
            if (DroneStatus[drone]) :
                answer = answer + "Available"
            else :
                answer = answer + "Unavailable"
            connectionSocket.send(answer.encode())      
            print(answer)
    except Exception as error:
        print (Exception,":",error)
        print ("Something went wrong\r\n")
router_client_socket.close()
connectionSocket.close()




def updateClient(Dictionary, socket):
    message = ""
    for drone in Dictionary:
        message = message + drone 
        if Dictionary[drone]:
            message = message+" is available "
        else:
            message = message+" is unavailable "