import sys
from socket import * 
import time

#TODO dizionario con indirizzi 
# Wrapper ip

connected_drones = 0;
max_drones = 3;

Etalide_Status = "unavailable"
Erito_Status = "unavailable"
Eudoro_Status = "unavailable"

Drone_Facing_IP = "192.168.1.0"
Client_Facing_IP = "10.10.10.1"

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


def droneHandler():
    def __init__(self,drone_adress,drone_socket):
      threading.Thread.__init__(self)
      self.csocket = drone_socket
      print ("New connection added: ", drone_adress)
    def run(self):
      print ("Connection from : ", drone_adress)
      #self.csocket.send(bytes("Hi, This is from Server..",'utf-8'))
      msg = ''
      while True:
          data = self.csocket.recv(2048)
          msg = data.decode()
          if msg=='bye':
            break
          print ("from client", msg)
          self.csocket.send(bytes(msg,'UTF-8'))
      print ("Client at ", drone_adress , " disconnected...")

# clientHandler()
# droneHandler()

server_drone_socket = socket(AF_INET, SOCK_DGRAM)
drone_address = ('localhost', IpToPort[DroneToIp["Etalide"]])
server_drone_socket.bind(drone_address)

while connected_drones <= max_drones:
    server_drone_socket.listen(3)
    drone_socket, drone_adress = server_drone_socket.accept()
    drone_thread = DroneHandler(drone_adress, drone_socket)
    drone_thread.start()
    drone_thread.join()
    server_drone_socket.close()
    
    
    

