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
	newMessage = ('Ping' + str(i + 1) + 'th message from Client').encode()
	sendTime = time.time()
	try:
		clientSocket.sendto(newMessage, serverAddr)
		backMessage, _ = clientSocket.recvfrom(2048)
		# calculate the RRT
		roundTripTime = time.time() - sendTime
		print('Sequence %d: RTT = %.5fs' %(i + 1, roundTripTime))
	except Exception as e:
		print('Sequence %d: Request time out' %(i + 1))
# close the client socket
clientSocket.close()