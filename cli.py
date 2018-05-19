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
		print("tmpBuff = ", tmpBuff)

		# Attempt to receive bytes
		tmpBuff =  sock.recv(numBytes)

		# The other side has closed the socket
		if not tmpBuff:
			break

		# Add the received bytes to the buffer
		recvBuff += str(tmpBuff)
		print("recvBuff = ", recvBuff)

	return recvBuff

#make sure there are enough command line arguments
if len(sys.argv) != 3:
    print("USAGE python3" , sys.argv[0] , " <server_machine> <server_port>")
    sys.exit()

#name and port number of the server to which we are connecting
serverName = sys.argv[1]
serverPort = sys.argv[2]
#resolve IP
serverIP = gethostbyname(serverName)

#create a serverSocket
clientSocket = socket(AF_INET, SOCK_STREAM)

#connect to the serverPort
serverPort = int(serverPort)
clientSocket.connect((serverIP, serverPort))

while True:
    #determine if client is still connected to server
    flag = clientSocket.recv(9)
    flag = int(flag)

    while flag == 1:
        #get user input
        cmd = input("ftp> ").split(" ")

        if cmd[0] == "get":
            if len(cmd) != 2:
                print("USAGE get <file_name>")
                clientSocket.close()
            else:
                clientSocket.sendall(cmd[0].encode('utf-8'))
                clientSocket.sendall(cmd[1].encode('utf-8'))
                print(cmd[0] , " " , cmd[1])

            #create ephemereal port
            #reference from Gofman's example code
            dataSocket = socket(AF_INET, SOCK_STREAM)
            dataSocket.bind("", 0)
            print("I choose ephemeral port: " , dataSocket.getsockname()[1])

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
            fileSize = recvAll(connectionSocket, 0)
            print("The file size is " , fileSize)
            fileSize = int(fileSize)

            #get file data
            fileData = recvAll(connectionSocket, fileSize)

            print(fileData)
            print("Saving to client.txt")

            outfile = open('client.txt', 'w')
            outfile.write(fileData)
            outfile.close()

            #close connection
            connectionSocket.close()

        elif cmd[0] == "put":
            clientSocket.sendall(cmd[0].encode('utf-8'))
            print("Sent: ", cmd[0])
            clientSocket.sendall(cmd[1].encode('utf-8'))
            file = cmd[1]
            file = open(file, 'r').read()
            clientSocket.sendall(file.encode('utf-8'))
            print("Sent: ", cmd[1])
        elif cmd[0] == "ls":
            clientSocket.sendall(cmd[0].encode('utf-8'))

            #the buffer to store server data
            servData = ""

            #the buffer to store size of incoming data
            servSize = ""

            #generate ephemeral port
            dataSocket = socket(AF_INET, SOCK_STREAM)
            dataSocket.bind(("", 0))
            print("I choose ephemeral port: " , dataSocket.getsockname()[1])
            clientSocket.send((str(dataSocket.getsockname()[1])).encode('utf-8'))
            dataSocket.listen(1)

            #accept connection from server
            connectionSocket, addr = dataSocket.accept()

            #get size of incoming data from server
            servSize = connectionSocket.recv(10)
            #print(servSize)
            servSize = int(servSize)
                

            #get the data from the server
            servData = connectionSocket.recv(10000).decode('utf-8')
            print("Size: " , servSize , "Received:")
            print(servData)

            #get flag from server
            flag = clientSocket.recv(9)
            connectionSocket.close()
            flag = 1

        elif cmd[0] == "lls":
            path = os.path.dirname(os.path.realpath(__file__))
            ls = os.listdir(path)
            print(ls)
        elif cmd[0] == "quit":
            command = cmd[0]
            clientSocket.sendall(command.encode('utf-8'))
            flag = clientSocket.recv(9)
            break
        elif cmd[0] == "":
            #if blank, do nothing
            pass
        else:
            print("Invalid command.")

    #break out of loop when server sends back any number != 1
    break
clientSocket.close()
print("Client connection closing")
