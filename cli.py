#client code
from socket import *
import sys
import os.path

# Gofman's sample code
# ************************************************
# Receives the specified number of bytes
# from the specified socket
# @param sock - the socket from which to receive
# @param numBytes - the number of bytes to receive
# @return - the bytes received
# *************************************************
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
if len(sys.argv) != 3:
    print "USAGE python3" + sys.argv[0] + " <server_machine> <server_port>"
    sys.exit()

#name and port number of the server to which we are connecting
serverName = sys.argv[1]
serverPort = sys.argv[2]

#create a serverSocket
clientSocket = socket(AF_INET, SOCK_STREAM)

#connect to the serverPort
clientSocket.connect((serverName, serverPort))

while True:
    #determine if client is still connected to server
    flag = clientSocket.recv(9)

    while flag == "1":
        #get user input
        cmd = input("ftp> ").split(" ")

        if cmd[0] == "get":
            if len(cmd) != 2:
                print "USAGE get <file_name>"
            else:
                clientSocket.send(cmd[0])
                clientSocket.send(cmd[1])
                print cmd[0] + " " + cmd[1]

            #create ephemereal port
            #reference from Gofman's example code
            dataSocket = socket(AF_INET, SOCK_STREAM)
            dataSocket.bind("", 0)
            print "I choose ephemeral port: " + dataSocket.getsockname()[1]

            #send the port number to server
            clientSocket.send(str(dataSocket.getsockname()[1]))
            dataSocket.listen(1)

            #accept a connections
            connectionSocket, addr = dataSocket.accept()

            #the buffer to store the file data
            fileData = ""

            #the buffer to store the size of the file
            fileSize = ""

            #receive first 10 bytes indicating file size
            fileSize = recvAll(connectionSocket, 10)
            print "The file size is " + fileSize
            fileSize = int(fileSize)

            #get file data
            fileData = recvAll(connectionSocket, fileSize)

            print fileData
            print "Saving to client.txt"

            outfile = open('client.txt', 'w')
            outfile.write(fileData)
            outfile.close()

            #close connection
            connectionSocket.close()

        elif command[0] == "put":
        elif command[0] == "ls":
            clientSocket.send(cmd[0])

            #the buffer to store server data
            servData = ""

            #the buffer to store size of incoming data
            servSize = ""

            #generate ephemeral port
            dataSocket = socket(AF_INET, SOCK_STREAM)
            dataSocket.bind("", 0)
            print "I choose ephemeral port: " + dataSocket.getsockname()[1]
            clientSocket.send(str(dataSocket.getsockname()[1]))
            dataSocket.listen(1)

            while 1:
                #accept connection from server
                connectionSocket, addr = dataSocket.accept()

                #get size of incoming data from server
                servSize = recvAll(connectionSocket, 10)
                servSize = int(servSize)

                #get the data from the server
                servData = recvAll(connectionSocket, servSize)

                print "Size: " + servSize + "Received:"
                print servData

                #get flag from server
                flag = clientSocket.recv(9)
                connectionSocket.close()

        elif cmd[0] == "lls":
        elif cmd[0] == "quit":
            clientSocket.send(cmd[0])
            flag = clientSocket.recv(9)
            break
        elif cmd[0] == "":
            #if blank, do nothing
            pass
        else:
            print "Invalid command."

    #break out of loop when server sends back any number != 1
    break
clientSocket.close()
print "Client connection closing"
