import random
from socket import *
import time

serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1)

RRTTotal = 0
numTotal = 0
RRTMax = 0
RRTMin = 1
for i in range(10):
    newMessage = str(i)
    for l in range(10):
        stand = random.randint(0, 26)
        c = chr(ord('a') + stand)
        newMessage += c
    sendMess = ('Ping %d %s ' % (i + 1, newMessage)).encode()
    sendTime = time.time()
    try:
        clientSocket.sendto(sendMess, (serverName, serverPort))
        modifiedMessage, serverAdress = clientSocket.recvfrom(2048)
        RTT = time.time() - sendTime
        RRTMin = min(RTT, RRTMin)
        RRTMax = max(RTT, RRTMax)
        RRTTotal += RTT
        numTotal += 1
        print('Sequence %d: Reply from %s  RTT = %.5fs' % (i + 1, serverName, RTT))
    except Exception as e:
        print('Sequence %d: Request timed out' % (i + 1))

print('RRTmin:%.3f RRTMax:%.3f rate:%.f averRTT:%.3f' % (
    RRTMin, RRTMax, numTotal / 10.0 , RRTTotal / numTotal))

clientSocket.close()
