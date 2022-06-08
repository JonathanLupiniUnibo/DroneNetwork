'''
                            UDP SERVER SOCKET
Corso di Programmazione di Reti - Laboratorio - Università di Bologna
G.Pau - A. Piroddi
'''

import socket as sk
import time


Eudoro_IP = "192.168.1.3"


# Creiamo il socket
sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)

# associamo il socket alla porta
server_address = ('localhost', 12003)
print ('\n\rstarting up on %s port %s' % server_address)
sock.bind(server_address)

while True:
    print('\n\rwaiting to receive message...')
    data, address = sock.recvfrom(4096)

    print('received %s bytes from %s' % (len(data), address))
    print (data.decode('utf8'))
    
    
    if data:
        data1="Etalide is online"
        time.sleep(2)
        sent = sock.sendto(data1.encode(), address)
        print ('sent %s bytes back to %s' % (sent, address))

