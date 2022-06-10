from socket import *
import threading
import time

#netstat -ano|findstr 10000

def updateClient():
    while True:
        time.sleep(5)
        message = ""
        for drone in DroneStatus:
            message = message + drone 
            if DroneStatus[drone]:
                message = message+" is available "
            else:
                message = message+" is unavailable "
                
def handleClient():           
    while True:
        print ('Ready to serve...')
        try:
            message = connectionSocket.recv(1024)
            if message.decode() == "END":
                answer = "Ending started"
                connectionSocket.send(answer.encode())
                router_client_socket.close()
                router_drone_socket.close()
                return
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
            print ("Something went wrong when talking to the client\r\n")
            router_client_socket.close()
            router_drone_socket.close()
            return
            
def droneListen():
    while True:
        print ("Listening to drones")
        try:
            message, droneAdress = router_drone_socket.recvfrom(1024)
            message = message.decode("utf-8")
            print("Drone said : "+message)
            drone = message.split()[0]
            status = message.split()[1]
            if status == "True":
                DroneStatus[drone] = False
            else:
                DroneStatus[drone] = True
        except Exception as error:
           print (Exception,":",error)
           print ("Something went wrong when listening to drone\r\n")    
           router_client_socket.close()
           router_drone_socket.close()
           return
             

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
   

print ('the router is facing the client on port:',client_facing_port)
print ('the router is facing the drones on port:',drone_facing_port)

drone_listen_thread = threading.Thread(target=droneListen)
drone_listen_thread.start()

router_client_socket.listen(0)
connectionSocket, addr = router_client_socket.accept()
print(connectionSocket)
print(addr)
client_thread = threading.Thread(target = handleClient)
client_thread.start();





