import sys
from socket import * 
import time

def clientHandler():
    serverSocket = socket(AF_INET, SOCK_STREAM)
    server_address=('localhost',10000)
    serverSocket.bind(server_address)

    serverSocket.listen(1)
    print ('the web server is up on port:',10000)

    while True:

        print ('Ready to serve...')
        connectionSocket, addr = serverSocket.accept()
        print(connectionSocket,addr)

        try:

            message = connectionSocket.recv(1024)
            connectionSocket.send("Hello to you too".encode())
            connectionSocket.close()
                

        except IOError:
     #Invia messaggio di risposta per file non trovato
            connectionSocket.send(bytes("Something went wrong","UTF-8"))
            connectionSocket.close()

def droneHandler():
    # Create il socket UDP
    sock = socket(AF_INET, SOCK_DGRAM)

    drone_adress = ('localhost', 12000)
    message = 'Send immediate assistance to Cadia'

    try:

        # inviate il messaggio
        print ('sending "%s"' % message)
        time.sleep(2) #attende 2 secondi prima di inviare la richiesta
        sent = sock.sendto(message.encode(), drone_adress)

        # Ricevete la risposta dal server
        print('waiting to receive from')
        data, server = sock.recvfrom(4096)
        #print(server)
        time.sleep(2)
        print ('received message "%s"' % data.decode('utf8'))
    except Exception as info:
        print(info)
    finally:
        print ('closing socket')
        sock.close()

# clientHandler()
droneHandler()

