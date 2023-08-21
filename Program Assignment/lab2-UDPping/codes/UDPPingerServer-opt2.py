# UDPPingerServer-opt2.py
# We will need the following module to generate randomized lost packets
import random
from socket import *
import time

# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)
# Assign IP address and port number to socket
serverSocket.bind(('localhost', 12000))

startTime = float(time.time())


while True:
    try:
        print("waiting....")
        # Receive the client packet along with the address it is coming from
        message, address = serverSocket.recvfrom(1024)
        # decode the message from the client
        message = message.decode().split(' ')
        startTime = float(message[4])
        PingTime = float(time.time()) - startTime
        print(message[0], ' ', message[1], PingTime)
    except Exception as e:
        print(e)
        if time.time() - startTime >= 1.0:
            print('HearBeat pause')
        else:
            print('package lost')
