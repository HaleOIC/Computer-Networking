import socket
import os
import sys
import struct
import select
import time

ICMP_ECHO_REQUEST = 8

# get the checksum of the target string
def checksum(string): 
	csum = 0
	countTo = (len(string) // 2) * 2 
	count = 0

	# sum all the value of the string
	while count < countTo:
		thisVal = string[count+1] * 256 + string[count]
		csum = csum + thisVal 
		csum = csum & 0xffffffff  			# truncate the outcome to 32bits
		count = count + 2

	# check out whether exists the last odd string 
	if countTo < len(string):
		csum = csum + string[len(string) - 1]
		csum = csum & 0xffffffff 

	# split the value into two part and add them all
	csum = (csum >> 16) + (csum & 0xffff)
	csum = csum + (csum >> 16)

	# get the complement value of the right now value	
	answer = ~csum 
	answer = answer & 0xffff 
	answer = answer >> 8 | (answer << 8 & 0xff00)

	# return back the value
	return answer

# receive one ping from the remote server
def receiveOnePing(mySocket, ID, timeout, destAddr):
	timeLeft = timeout

	while True: 
		startedSelect = time.time()
		whatReady = select.select([mySocket], [], [], timeLeft)
		howLongInSelect = (time.time() - startedSelect)
		if whatReady[0] == []: # Timeout
			return "Request timed out."
		
		timeReceived = time.time() 
		recPacket, addr = mySocket.recvfrom(1024)

		#Fetch the ICMP header from the IP packet
		header = recPacket[20:28]
		header_type, header_code, header_checksum, header_packet_ID, header_sequence = struct.unpack("bbHHh", header)

		# according to the header_type and header_code to determine the feedback message
		if(header_type != 0 or header_code != 0 or header_packet_ID != ID or header_sequence != 1):
			if header_type == 3 and header_code == 0:
				return 'Destination network unreachable'
			elif header_type == 3 and header_code == 1:
				return 'Destination host unreachable'
			elif header_type == 3 and header_code == 2:
				return 'Destination protocol unreachable'
			elif header_type == 3 and header_code == 3:
				return 'Destination port unreachable'
			elif header_type == 3 and header_code == 6:
				return 'Destination network unknown'
			elif header_type == 3 and header_code == 7:
				return 'Destination host unknown'
			elif header_type == 4 and header_code == 0:
				return 'Source quench'
			elif header_type == 12 and header_code == 0:
				return 'IP header corruption'
			else:
				return "Receive error."
 
        # calculate the new timeLeft
		timeLeft = timeLeft - howLongInSelect
		if timeLeft <= 0:
			return "Request timed out."

		return 1 - timeLeft

# send one ping to the remote server
def sendOnePing(mySocket, destAddr, ID):
	# Header is type (8), code (8), checksum (16), id (16), sequence (16)
	myChecksum = 0

	# Make a dummy header with a 0 checksum
	# struct -- Interpret strings as packed binary data
	header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
	data = struct.pack("d", time.time())

	# Calculate the checksum on the data and the dummy header.
	myChecksum = checksum(header + data)
	
	# Get the right checksum, and put in the header
	if sys.platform == 'darwin':
		# Convert 16-bit integers from host to network byte order
		myChecksum = socket.htons(myChecksum) & 0xffff
	else:
		myChecksum = socket.htons(myChecksum)
	

	header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
	packet = header + data

	mySocket.sendto(packet, (destAddr, 1)) # AF_INET address must be tuple, not str
	# Both LISTS and TUPLES consist of a number of objects
	# which can be referenced by their position number within the object.


def doOnePing(destAddr, timeout): 
	icmp = socket.getprotobyname("icmp")
	# SOCK_RAW is a powerful socket type. For more details: http://sock-raw.org/papers/sock_raw
	
	mySocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
	
	myID = os.getpid() & 0xFFFF # Return the current process i
	sendOnePing(mySocket, destAddr, myID)
	delay = receiveOnePing(mySocket, myID, timeout, destAddr)
	
	mySocket.close()
	return delay


def ping(host, timeout=1):
	# timeout=1 means: If one second goes by without a reply from the server,
	# the client assumes that either the client's ping or the server's pong is lost
	dest = socket.gethostbyname(host)
	print("Pinging " + host + '[' + dest + ']' + " using Python:")
	print("")
	totNum, lost, delayList = 0, 0, []
	# Send ping requests to a server separated by approximately one second
	try:
		while True :
			totNum += 1
			delay = doOnePing(dest, timeout)
			if type(delay) == float: 
				print('Reply from', dest, ': time = {:.4f}'.format(delay * 1000), 'ms')
				delayList.append(delay)
			else:
				lost += 1
				print(delay)
			time.sleep(1)# one second
	except KeyboardInterrupt:
		print('\nstatictics information of', dest)
		print('  packet: sent =', totNum, 'received =', totNum - lost, 'lost =', lost, '(', 100.0 * lost / totNum , '% )')
		if len(delayList) == 0:
			return
		print('Round Trip Time/RTT (ms):')
		print('  minimum = {:.4f} ms,'.format(min(delayList) * 1000), 'maxmimum = {:.4f} ms,'.format(max(delayList) * 1000), 'average = {:.4f} ms'.format(1000 * sum(delayList) / len(delayList)))


ping("www.qq.com")