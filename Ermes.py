from socket import *
import threading
import time

client_facing_port = 10000
drone_facing_port = 12000
router_client_socket = socket(AF_INET, SOCK_STREAM)
router_client_socket.bind(("localhost", client_facing_port))

Etalide = False;

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
    "Etalide" : False,
    "Erito" : False,
    "Eudoro" : False
    }

print ('the router is up on port:',client_facing_port)

router_client_socket.listen(0);

while True:

    print ('Ready to serve...')
    connectionSocket, addr = router_client_socket.accept()
    print(connectionSocket)
    print(addr)
    try:

        message = connectionSocket.recv(1024) ## riceve il messaggio di richiesta dal client
        drone = message.decode().split()[0]
        if (drone == "Etalide"):
            DroneStatus[drone] = not DroneStatus[drone];
            answer = "Etalide is now "  
            if (DroneStatus[drone]) :
                answer = answer + "Available"
            else :
                answer = answer + "Unavailable"
            connectionSocket.send(answer.encode())          
    except IOError:
 #Invia messaggio di risposta per file non trovato
        connectionSocket.send(bytes("HTTP/1.1 404 Not Found\r\n\r\n","UTF-8"))
        connectionSocket.send(bytes("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n","UTF-8"))
        connectionSocket.close()
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