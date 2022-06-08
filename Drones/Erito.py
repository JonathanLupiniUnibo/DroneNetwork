'''
                            UDP SERVER SOCKET
Corso di Programmazione di Reti - Laboratorio - Università di Bologna
G.Pau - A. Piroddi
'''

import socket as sk    #should probably have a different thread pinging the server
import time            #every 0.5 seconds with the drone's status

status = "available"


Erito_IP = "192.168.1.2"


# Creiamo il socket
sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)

# associamo il socket alla porta
server_address = ('localhost', 12002)
print ('\n\rstarting up on %s port %s' % server_address)
sock.bind(server_address)


while True:
        print('\n\rwaiting to receive message...')
        data, address = sock.recvfrom(4096)
        notify = sock.sendto(status.encode(), address)
        print('received %s bytes from %s' % (len(data), address))
        print (data.decode('utf8'))
        status == "unavailable"
        notify = sock.sendto(status.encode(), address)
        sleep(2)
        status = "available"
        

