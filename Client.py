'''
Corso di Programmazione di Reti - Laboratorio - Università di Bologna
Socket_Programming_Assignment - WebServer - G.Pau - A. Piroddi

Per eseguire il presente codice è necessario utilizzare o una Command Prompt o dal tab Run selezionare Run...Customized

'''
import socket as sk
import sys

clientsocket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)

host = "localhost"
port = 10000
message = "Hello"
try:
    clientsocket.connect((host,port))
except Exception as data:
    print (Exception,":",data)
    print ("Ritenta sarai più fortunato.\r\n")
    sys.exit(0)
clientsocket.send(message.encode()) #se tutto è andato bene, rispondiamo al servere con un 200 OK
print(message.encode())   
response = clientsocket.recv(1024)
    
print (response)
    
clientsocket.close()



