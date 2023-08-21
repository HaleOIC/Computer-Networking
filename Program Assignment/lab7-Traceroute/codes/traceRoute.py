from socket import *
import os
import sys
import struct
import time
import select
import binascii

ICMP_ECHO_REQUEST = 8
MAX_HOPS = 30
TIMEOUT= 2.0
TRIES= 2
# The packet that we shall send to each router along the path is the ICMP echo
# request packet, which is exactly what we had used in the ICMP ping exercise.
# We shall use the same packet that we built in the Ping exercise

# In this function we make the checksum of our packet
# hint: see icmpPing lab
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


# In the sendOnePing() method of the ICMP Ping exercise ,firstly the header of our
# packet to be sent was made, secondly the checksum was appended to the header and
# then finally the complete packet was sent to the destination.
# Make the header in a similar way to the ping exercise.
# Append checksum to the header.
# Don’t send the packet yet , just return the final packet in this function.
def build_packet():
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

	return packet



def get_route(hostname):
	timeLeft = TIMEOUT
	for ttl in range(1,MAX_HOPS):
		for tries in range(TRIES):
			destAddr = gethostbyname(hostname)

			# Make a raw socket named mySocket
			mySocket = socket(AF_INET, SOCK_RAW)			
			
			mySocket.setsockopt(IPPROTO_IP, IP_TTL, struct.pack('I', ttl))
			mySocket.settimeout(TIMEOUT)
			try:
				d = build_packet()
				mySocket.sendto(d, (hostname, 0))
				t= time.time()
				startedSelect = time.time()
				whatReady = select.select([mySocket], [], [], timeLeft)
				howLongInSelect = (time.time() - startedSelect)
				if whatReady[0] == []: # Timeout
					print("*	*	*	Request timed out.")
				recvPacket, addr = mySocket.recvfrom(1024)
				timeReceived = time.time()
				timeLeft = timeLeft - howLongInSelect
				if timeLeft <= 0:
					print("*	*	*	Request timed out.")
			except timeout:
				continue
			else:
				#Fetch the icmp type from the IP packet
				types = struct.unpack('B', recvPacket)
				if types == 11:
					bytes = struct.calcsize("d")
					timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
					print("	%d 	 rtt=%.0f ms 	%s" %(ttl, (timeReceived -t)*1000, addr[0]))
				elif types == 3:
					bytes = struct.calcsize("d")
					timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
					print("	%d  rtt=%.0f ms 	%s" %(ttl, (timeReceived-t)*1000, addr[0]))
				elif types == 0:
					bytes = struct.calcsize("d")
					timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
					print(" %d 	rtt=%.0f ms 	%s" %(ttl, (timeReceived - timeSent)*1000, addr[0]))
					return
				else:
					print("error")
				break
			finally:
				mySocket.close()
get_route("google.com")