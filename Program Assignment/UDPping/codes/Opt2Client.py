from socket import *
import time

serverName = 'localhost'
serverPort = 13
clientSocket = socket(AF_INET, SOCK_DGRAM)
for i in range(10):
    stime = time.time()
    message = str(i+1) + ' ' + str(stime)
    clientSocket.sendto(message.encode(), (serverName, serverPort))

clientSocket.close()
