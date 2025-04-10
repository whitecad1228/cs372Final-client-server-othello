import random
from socket import *
from Othello import Othello
from random import randint
"""
Soucres:
https://www.w3schools.com/python/python_strings_slicing.asp
https://www.geeksforgeeks.org/python-try-except/
https://docs.python.org/3/library/socket.html
https://docs.python.org/3/library/exceptions.html#EOFError
https://www.w3schools.com/python/ref_random_randint.asp
https://www.geeksforgeeks.org/python-list-of-tuples-to-string/
https://www.geeksforgeeks.org/socket-programming-python/
"""

# will get the data packet received from the socket and translate it.
def receiveData(res):
    x = res.split(">", 1)
    length = x[0][1:]
    data = x[1]
    if length == 0:
        data = None
    string = res.split()
    return data


if __name__ == '__main__':
    # creates a new server socket
    s = socket(AF_INET,SOCK_STREAM)
    #binds the server address and port to the socket
    s.bind(('127.0.0.1', 12000))
    s.listen(1)
    print("ready")

    #waits for a process to reach out
    while True:
        #gets the socket and its address
        connectionSocket, addr = s.accept()
        print(addr)
        #gets the message from the socket
        res = connectionSocket.recv(1024).decode()
        print(res)
        data = b"Connceted\r\n\r\n"
        print(data)
        #sends the data above
        connectionSocket.send(data)


        #insurtions and player name
        data = b"othello by Caden White\r\n" \
               b"before you start an intro...\r\n" \
               b"in the game first the board will appear, you will then be shown the board, then the available placements\r\n" \
               b"in an x,y position with the top left corner being 1,1 and the bottom right 8,8.\r\n" \
               b"after you will be shown the board but with ? where you can place a piece\r\n" \
               b"and then you will be prompted to put a piece down where you will reply with a x,y ie. 3,4\r\n" \
               b"To quit enter /q at amy time." \
               b"Would you like to play y/n: \r\n"
        connectionSocket.send(data)
        res = connectionSocket.recv(4096).decode()
        playerPlays = receiveData(res)
        #full game loop
        while playerPlays == "Yes" or playerPlays == "yes" or playerPlays == "Y" or playerPlays == "y":
            # game creation and player creation
            game = Othello()
            data = b"what is your name, you will be black or X: "
            connectionSocket.send(data)
            res = connectionSocket.recv(4096).decode()
            game.create_player(res,"black")
            #white create player
            game.create_player("Computer", "white")
            #turn based game loop
            playerTurn = "black"
            playerQuit = False
            while game.check_win() and not playerQuit:
                data = ""
                #board
                data += game.board_to_string()
                data += "\r\n"
                #players move
                data += "It is " + playerTurn + "'s turn.\r\n"
                playerMove = ()
                if playerTurn == "black":
                    #avalible moves
                    list = game.return_available_positions(playerTurn)
                    data += ', '.join([str(t) for t in list])
                    data += "\r\n"
                    #avalible moves board
                    data += game.available_positions_to_text(playerTurn)
                    data += "\r\n"
                    data += "What is your move in the form of x,y:\r\n"
                    connectionSocket.send(str.encode(data))
                    # get players move and error handle
                    res = connectionSocket.recv(4096).decode()
                    res = receiveData(res)
                    if res is not None:
                        try:
                            playerMove = tuple(map(int, res.split(',')))
                        except ValueError:
                            print("not a valid input")
                    if res == "/q":
                        playerQuit = True
                else:
                    #white AI move
                    positions = game.return_available_positions("white")
                    whitePosition = random.randint(0,len(positions)-1)
                    playerMove = positions[whitePosition]
                    # added player check to slow down game.
                    data += "Press enter to Continue:"
                    connectionSocket.send(str.encode(data))
                    res = connectionSocket.recv(4096).decode()
                    res = receiveData(res)
                    if res == "/q":
                        playerQuit = True

                #make move
                availableSpaces = game.return_available_positions(playerTurn)
                if playerMove in availableSpaces:
                    game.make_move(playerTurn, playerMove)
                    if playerTurn == "black":
                        if game.return_available_positions("white") != []:
                            playerTurn = "white"
                        else:
                            playerTurn = "black"
                    elif playerTurn == "white":
                        if game.return_available_positions("black") != []:
                            playerTurn = "black"
                        else:
                            playerTurn = "white"
                else:
                    if playerQuit != True:
                        data += "not a possible move, try again\r\n"
                        print("not a possible move, try again")

            #check player continue or new game
            data = ''
            if not game.check_win():
                data = game.return_winner()
            data += "\r\n Would you like to play again y/n:"
            connectionSocket.send(str.encode(data))
            playerPlays = connectionSocket.recv(4096).decode()

        #closes connecting socket
        connectionSocket.send(b'')
        #closes the connecting socket
        connectionSocket.close()