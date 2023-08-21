from socket import *
import time

# define the related server name, port and client socket
serverName = 'localhost'
serverPort = 12000
serverAddr = (serverName, serverPort)
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1)

for i in range(10):
	# generate the new message 
	newMessage = ('Ping' + str(i + 1) + 'th message from Client ').encode()
	newMessage += str(time.time()).encode()
    # send the send time to the server
	clientSocket.sendto(newMessage, serverAddr)
		
# close the client socket
clientSocket.close()