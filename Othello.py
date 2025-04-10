# Author: Caden White
# GitHub username:Whitecad1228
# Date: 5/27/2023
# Description: A complete text based version of the game othello
# the game is full functioning but i added play_full_game which once called will play a full othello
# game using all the functions created in the assignment, much better experience to play it that way.
class Othello:
    def __init__(self):
        self._board = [["*", "1", "2", "3", "4", "5", "6", "7", "8", "*"],
                        ["1", ".", ".", ".", ".", ".", ".", ".", ".", "*"],
                        ["2", ".", ".", ".", ".", ".", ".", ".", ".", "*"],
                        ["3", ".", ".", ".", ".", ".", ".", ".", ".", "*"],
                        ["4", ".", ".", ".", "O", "X", ".", ".", ".", "*"],
                        ["5", ".", ".", ".", "X", "O", ".", ".", ".", "*"],
                        ["6", ".", ".", ".", ".", ".", ".", ".", ".", "*"],
                        ["7", ".", ".", ".", ".", ".", ".", ".", ".", "*"],
                        ["8", ".", ".", ".", ".", ".", ".", ".", ".", "*"],
                        ["*", "*", "*", "*", "*", "*", "*", "*", "*", "*"]]
        self._piece_dict = {
            "white": "O",
            "black": "X",
            "white opposite": "X",
            "black opposite": "O",
            "edge": "*",
            "empty": "."

        }
        self._player_dict = {}

    #will play one full game
    def play_full_game(self):
        print("othello by Caden White")
        print("before you start an intro...")
        print("in the game first the board will appear, you will then be shown the board, then the available placements")
        print("in an x,y position with the top left corner being 1,1 and the bottom right 8,8.")
        print("after you will be shown the board but with ? where you can place a piece")
        print("and then you will be prompted to put a piece down where you will reply with a x,y ie. 3,4")
        print("To play enter your names...")
        first_player_name = input("what is the first players name, he will be black: ")
        self.create_player(first_player_name,"black")
        second_player_name = input("what is the first players name, he will be white: ")
        self.create_player(second_player_name,"white")

        player_turn = "black"
        while self.check_win():
            self.print_board()
            print(self.return_available_positions(player_turn))
            self.show_available_positions(player_turn)
            while(True):
                name = self._player_dict.get(player_turn).return_name()
                string = "what is " + name + "'s move:"
                player_move_string = input(string)
                player_move = tuple(map(int, player_move_string.split(',')))
                available_spaces = self.return_available_positions(player_turn)
                print(available_spaces)
                if player_move in available_spaces:
                    self.make_move(player_turn, player_move)
                    if player_turn == "black":
                        if self.return_available_positions("white") != []:
                            player_turn = "white"
                        else :
                            player_turn = "black"
                        break
                    elif player_turn == "white":
                        if self.return_available_positions("black") != []:
                            player_turn = "black"
                        else:
                            player_turn = "white"
                        break
                    else:
                        break
                else:
                    print("not a possible move, try again")
                    break
        print(self.return_winner())
        return

    #makes a turn in the game
    def play_game(self, color, position):
        #cords are in a tuple
        #postion is in x,y
        available_spaces = self.return_available_positions(color)
        good_move = False
        for space in available_spaces:
            if space == position:
                good_move = True
        if good_move:
            self.make_move(color, position)
        else:
            #print(position, " not a valid space")
            print("Here are the valid moves:", available_spaces)
            return "invalid move"
        if self.check_win():
            self.return_winner()

    #will return all availible positions of a color either black or white
    def return_available_positions(self, color):
        pieces = self.get_peices(self._piece_dict.get(color))
        total_available = []
        for piece in pieces:
            spaces = self.check_lines(piece[0], piece[1], self._piece_dict.get(color + " opposite"))
            for space in spaces:
                if space not in total_available:
                    total_available.append(space)
        total_available.sort()
        return total_available

        # prints a board showing the availible postions with a ?
    def show_available_positions(self, color):
        available_positions = self.return_available_positions(color)
        temp_board = []
        for y in range(0, len(self._board)):
            temp_board.append(self._board[y].copy())
            for x in range(0, len(temp_board[y])):
                for position in available_positions:
                    if (x, y) == position:
                        temp_board[y][x] = "?"
        for rows in temp_board:
            for column in rows:
                print(column, end=" ")
            print()
        return

    def available_positions_to_text(self,color):
        available_positions = self.return_available_positions(color)
        temp_board = []
        for y in range(0, len(self._board)):
            temp_board.append(self._board[y].copy())
            for x in range(0, len(temp_board[y])):
                for position in available_positions:
                    if (x, y) == position:
                        temp_board[y][x] = "?"
        board = ""
        for rows in temp_board:
            for column in rows:
                board += column
            board += "\r\n"
        return board

    #returns a list of tuples holding the postion of each color peice on the board
    def get_peices(self, marker):
        pieces = []
        for y in range(0,len(self._board)):
            for x in range(0, len(self._board[y])):
                if self._board[y][x] == marker:
                    pieces.append((x,y))
        return pieces

    #checks each line from a x,y and stops at marker
    def check_lines(self,x,y,marker):
        possible_postions = []
        #y's
        for rows in range(-1, 2):
            #x's
            for columns in range(-1, 2):
                inc = 1
                if columns != 0 or rows != 0:
                    while self._board[y + (rows*inc)][x + (columns*inc)] != "*":
                        if self._board[y + (rows * inc)][x + (columns * inc)] == marker and self._board[y + (rows * (inc+1))][x + (columns * (inc+1))] == ".":
                            possible_postions.append((x + (columns * (inc+1)), y + (rows * (inc+1))))
                        if self._board[y + (rows * (inc))][x + (columns * (inc))] == ".":
                            break
                        inc += 1
        return possible_postions
    #places a peice of a color at position
    def make_move(self,color,position):
        print()
        self._board[position[1]][position[0]] = self._piece_dict.get(color)
        self.flip_pieces(position[0],position[1], color)
        return self._board

    #flips all the required pieces of piece x,y
    def flip_pieces(self,x,y,color):
        # y's
        for rows in range(-1, 2):
            # x's
            for columns in range(-1, 2):
                inc = 1
                if columns != 0 or rows != 0:
                    flip_row = False
                    while self._board[y + (rows * inc)][x + (columns * inc)] != "*":
                        if self._board[y + (rows * inc)][x + (columns * inc)] == self._piece_dict.get(color):
                            flip_row = True
                            break
                        if self._board[y + (rows * inc)][x + (columns * inc)] == ".":
                            break
                        inc += 1
                    if flip_row:
                        inc = 1
                        while self._board[y + (rows * inc)][x + (columns * inc)] != self._piece_dict.get(color):
                            self._board[y + (rows * inc)][x + (columns * inc)] = self._piece_dict.get(color)
                            inc += 1
        return
    #prints the board
    def print_board(self):
        for rows in self._board:
            for column in rows:
                print(column, end=" ")
            print()

    def board_to_string(self):
        board = ""
        for rows in self._board:
            for column in rows:
                board += column
            board += "\r\n"
        return board



    #creates a new player and saves it in the player dict
    def create_player(self, player_name, color):
        ind_player = Player(player_name,color)
        self._player_dict.update({color : ind_player})
        return
    #returns the winner
    def return_winner(self):
        black_total = 0
        white_total = 0
        for y in range(0, len(self._board)):
            for x in range(0, len(self._board[y])):
                if self._board[y][x] == self._piece_dict.get("black"):
                    black_total += 1
                if self._board[y][x] == self._piece_dict.get("white"):
                    white_total += 1
        if black_total > white_total:
            return "Winner is black player: " + self._player_dict.get("black").return_name() \
                + " with " + str(black_total) + " pieces vs " + str(white_total) + " pieces"
        elif white_total > black_total:
            return "Winner is white player: " + self._player_dict.get("white").return_name() \
                + " with " + str(white_total) + " pieces vs " + str(black_total) + " pieces"

        else:
            return "It's a tie " + str(white_total) + " white pieces vs " + str(black_total) + " black pieces"

    #determines if there is a possible move among black or white
    def check_win(self):
        white = self.return_available_positions("white")
        black = self.return_available_positions("black")
        if white == [] and black == []:
            return False
        else:
            return True

#player class
class Player():
    #defines player name and color
    def __init__(self, player_name, color):
        self._player_name = player_name
        self._color = color
    #returns the players color
    def return_color(self):
        return self._color
    #returns the players name
    def return_name(self):
        return self._player_name
def main():
    game = Othello()
    print(game.board_to_string())
    #game.play_full_game()

    # game.print_board()
    # game.create_player("Helen", "white")
    # game.create_player("Leo", "black")
    # game.show_available_positions("black")
    # print(game.return_available_positions("black"))
    # game.play_game("black",(6,9))
    # game.print_board()
    #
    # game.show_available_positions("white")
    # print(game.return_available_positions("white"))
    # game.print_board()
    # game.play_game("white",(6, 6))
    #
    # game.print_board()
    # print(game.return_available_positions("black"))
    # game.show_available_positions("black")
    # game.play_game("black", (3, 4))
    #
    # print(game.return_available_positions("white"))
    # game.show_available_positions("white")
    # game.play_game("white", (4, 6))
    # game.print_board()
    #
    # print(game.return_available_positions("black"))
    # game.show_available_positions("black")
    # game.play_game("black", (7, 7))
    # game.print_board()
    #
    # print(game.return_available_positions("white"))
    # game.show_available_positions("white")
    # game.play_game("white", (2, 3))
    # game.print_board()
    #
    # print(game.return_available_positions("black"))
    # game.show_available_positions("black")
    # game.play_game("black", (3, 6))
    # game.print_board()
    #
    # print(game.return_available_positions("white"))
    # game.show_available_positions("white")

if __name__ == '__main__':
    main()