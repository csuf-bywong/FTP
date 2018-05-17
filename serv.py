from socket import *
import os
import sys

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
serverSocket = socket(AF_INET, SOCK_STREAM)

#bind the socket to the serverPort
serverSocket.bind(('', serverPort))

#start listening for connections
serverSocket.listen(1)

print("The server is ready to receive")

#forever accept incoming connections
while 1:
    #accept a connection; get client's serverSocket
    connectionSocket, addr = serverSocket.accept()

    #tell client server is ready for commands
    connectionSocket.send("1")

    #forever accept incoming commands
    while 1:
        #receive command from client
        cmd = connectionSocket.recv(4)

        if cmd == "quit":
            print("received " , cmd)
            connectionSocket.send("0")
            break

        elif command == "ls":
            ephPort = int(connectionSocket.recv(10))
            print("Received ephemeral port: " , ephPort)

            #create connection for data transfer
            servDataSock = socket(AF_INET, SOCK_STREAM)
            servDataSock.connect(("localhost", ephPort))

            #get path
            path = os.path.dirname(os.path.realpath(__file__))

            #get dir file lis
            ls = os.listdir(path)

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

            bytesSent = 0

            #send the data
            while len(lst) > bytesSent:
                bytesSent += servDataSock.send(lst[bytesSent:])

            #close connection
            servDataSock.close()
            #say server is ready for another command
            connectionSocket.send("1")
