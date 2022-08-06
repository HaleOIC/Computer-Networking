from socket import *
import time

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverPort = 13
serverSocket.bind(('', serverPort))


start_time = float(time.time())
end_time = start_time

while True:

    try:
        serverSocket.settimeout(0.1)
        message, address = serverSocket.recvfrom(1024)
        message = message.decode()
        rtime = float(message.split()[1])
        start_time = rtime
        Ping = float(time.time())-rtime
        print(str(message.split()[0])+':',Ping)

    except Exception as e:
        if end_time == start_time:
            continue
        if time.time()-start_time >= 1.0:
            print('Heartbeat pause')
            break
        else:
            print('Packet lost')
