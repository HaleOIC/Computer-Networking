from socket import *

serverName = '192.168.1.107'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
sentence = input('Input lowercase sentence:\n')
clientSocket.send(sentence.encode())
modifiedSentence = clientSocket.recv(1024).decode()
print('From Server: ', modifiedSentence)
clientSocket.close()
