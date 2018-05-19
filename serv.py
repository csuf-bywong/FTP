import socket
#from socket import *
import os
import sys
from os import listdir

def recvAll(sock, numBytes):
	# The buffer
	recvBuff = ""

	# The temporary buffer
	tmpBuff = ""

	# Keep receiving till all is received
	while len(recvBuff) < numBytes:

		# Attempt to receive bytes
		tmpBuff =  sock.recv(numBytes)

		# The other side has closed the socket
		if not tmpBuff:
			break

		# Add the received bytes to the buffer
		recvBuff += tmpBuff

	return recvBuff

#make sure there are enough command line arguments
if len(sys.argv) != 2:
    print("USAGE python3 " , sys.argv[0] , " <port_number>")
    sys.exit()

#the port on which to listen
serverPort = int(sys.argv[1])

#create a TCP socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#bind the socket to the serverPort
serverSocket.bind(('', serverPort))

#start listening for connections
serverSocket.listen(100)

print("The server is ready to receive")

#forever accept incoming connections
while 1:
    #accept a connection; get client's serverSocket
    connectionSocket, addr = serverSocket.accept()

    #tell client server is ready for commands
    connectionSocket.sendall("1".encode('utf-8'))

    #forever accept incoming commands
    while 1:
        cmd = connectionSocket.recv(4)
        print("cmd = ", cmd)
        cmd = str(cmd)
        cmd = cmd[2:-1]

        if cmd == "quit":
            print("received " , cmd)
            connectionSocket.sendall("0".encode('utf-8'))
            break

        elif cmd == "ls":
            ephPort = int(connectionSocket.recv(10))
            print("Received ephemeral port: " , ephPort)

            #create connection for data transfer
            servDataSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            servDataSock.connect(("localhost", ephPort))
            
            #get path
            path = os.path.dirname(os.path.realpath(__file__))
            #get dir file lis
            ls = str(os.listdir(path))
            #var to store the list
            lst = ""
            for value in ls:
                lst = lst + value + '\n'

            #get size of data
            size = str(len(lst))

            #convert to 10 byte header
            while len(size) < 10:
                size = "0" + size

            #attach size to beginning of data
            lst = size + lst

            bytesSent = 1

            #send the data
            lenls = len(ls)
            #while len(ls) > bytesSent:
            servDataSock.sendall(str(lenls).encode('utf-8'))
            servDataSock.sendall(str(ls).encode('utf-8'))
            print("bytesSent = ", bytesSent)

            servDataSock.close()
            #say server is ready for another command
            connectionSocket.sendall(b"\"1\"")
