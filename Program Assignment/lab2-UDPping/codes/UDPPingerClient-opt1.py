from socket import *
import time

# define the related server name, port and client socket
serverName = 'localhost'
serverPort = 12000
serverAddr = (serverName, serverPort)
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1)

# used for calculating the average RRT and package loss rate
minRRT, maxRRT, totRRT, totNum = 1.0, 0.0, 0.0, 0,


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
		minRRT = min(minRRT, roundTripTime)
		maxRRT = max(maxRRT, roundTripTime)
		totRRT += roundTripTime
		totNum += 1
	except Exception as e:
		print('Sequence %d: Request time out' %(i + 1))
# close the client socket
clientSocket.close()

# print out some messages
print('\n Max RRT is %.5f, Min RRT is %.5f, Average RRT is %.5f,\n \
	package loss rate is %.5f%%' %(maxRRT, minRRT, totRRT / totNum, ( 1.0 - 1.0 * totNum / 10) * 100 ))