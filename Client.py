from socket import *

if __name__ == '__main__':
    #creates a new socket
    s = socket()

    # connect to the server on local computer
    s.connect(('127.0.0.1', 12000))
    #sends a HTTP get request to the server, gaia.cs.umass.edu
    s.send(b"connecting\r\n\r\n")
    #get the recvied message and decodes it
    recived = s.recv(1024).decode()
    #prints what was recived
    print(recived)


    while len(bytes(recived, 'utf-8')) > 0:
        recived = s.recv(4096).decode()
        print(recived)
        playerInput = input()
        # sends a packet with the form <length>data IE. <1>Y
        s.send(str.encode("<" + str(len(playerInput)) + ">" + playerInput))

    if len(bytes(recived, 'utf-8')) <= 0:
        print("closing socket")

    # closes the connection
    s.close()