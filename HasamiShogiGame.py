# Author: Mark Hager
# Date: 11/22/2021
# Description: Variant 1 Hasami Shogi Game with the following rules:
# https://en.wikipedia.org/wiki/Hasami_shogi#Variant_1

# import our Pygame classes to render the game
from PyGameRenderer import *


class HasamiShogiGame:
    """
    Represents a game of Hasami Shogi, with methods to initialize and print the board, pawn position,
    pawn captures and removals and tracking player turn and game state.
    """
    def __init__(self):
        """
        Creates a new game of Hasami Shogi with private data members for the game state, the player turn,
        and the number of captured pieces per player.
        """
        # initialize the new game as unfinished
        self._game_state = 'UNFINISHED'
        # used to create and display the board
        self._row_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
        # initialize the board as dictionary with 81 items by calling create_board method
        self._board = self.create_board()
        # initialize player turn to Black as they always start
        self._active_player = "BLACK"
        # initialize dictionary to hold how many pieces lost by each player
        self._captured_pieces = {
                                  "BLACK": 0,
                                  "RED": 0,
                                 }
    def create_board(self):
        """
        Create the game board using a dictionary. The keys of each item use
        algebraic notation such that the first item key is a1. The value of each item
        represents whether that square is occupied by either color of pawn or is unoccupied.
        """
        # create a new dictionary to hold the squares
        new_board = {}
        # list of the row letters to iterate through
        for letter in self._row_letters:
            for col_num in range(1, 10):
                # fill the top row with Red pawns
                if letter == 'a':
                    new_board[letter + str(col_num)] = 'R'
                # fill the bottom row with Black pawns
                elif letter == 'i':
                    new_board[letter + str(col_num)] = 'B'
                # the rest of the board starts empty
                else:
                    new_board[letter + str(col_num)] = '.'

        return new_board

    def get_game_state(self):
        """
        Gets the state of the game. Returns either 'UNFINISHED', 'RED_WON' or 'BLACK_WON'
        """
        return self._game_state

    def get_active_player(self):
        """
        Returns which player's turns it is - returns either 'RED' or 'BLACK'
        """
        return self._active_player

    def get_num_captured_pieces(self, player):
        """
        Returns the number of pieces captured belonging to either player
        'RED' or 'BLACK' depending on the argument.
        """
        # obtain the value by using the player color argument as the key
        num_of_pieces = self._captured_pieces.get(player)
        # return the value as the number of captured pieces
        return num_of_pieces

    def make_move(self, origin, destination):
        """
        Takes the position of a piece and its intended destination as parameters.
        Calls test_move using parameters, if move is illegal then make_move returns False.
        Else complete the move and remove any captured pieces and update the game status and player turn
        if necessary and return True.
        """
        # check that the game is still unfinished
        if self._game_state == "UNFINISHED":
            check_move = self.test_move(origin, destination)
            if check_move is True:
                # move pawn from origin to destination
                pawn = self._board.get(origin)
                self._board[origin] = '.'
                self._board[destination] = pawn

                # check for captures
                capture_list = self.check_captures(destination)
                # remove captures from board
                if capture_list is not None:
                    for capture in capture_list:
                        self._board[capture] = '.'

                self.update_turn()
                return True
        # if check_move failed or game is over
        return False

    def test_move(self, origin, destination):
        """
        Method called by make_move to check if move is legal. Checks that a pawn exists at the origin square
        and that destination is either horizontal or vertical to origin. Also checks to make sure
        there is no collision with other pieces. If move is legal returns True else returns False.
        """
        # check that pawn at origin belongs to player making move
        origin_check = self.get_square_occupant(origin)
        # check that the destination is unoccupied
        destination_check = self.get_square_occupant(destination)

        if origin_check == self.get_active_player() and destination_check == 'NONE':
            # check that destination is on either the same row or column as origin
            if origin[0] == destination[0]:  # origin and destination are on same row

                # compare column numbers to determine if we're going left or right
                origin_y = int(origin[1])
                destination_y = int(destination[1])

                if origin_y < destination_y:
                    # if origin is adjacent to clear destination then return True
                    if origin_y + 1 == destination_y:
                        return True
                    # check all squares between origin and destination from left to right
                    for col in range(origin_y + 1, destination_y):
                        step = self.get_square_occupant(origin[0]+str(col))
                        # if there is another pawn in the way
                        if step != 'NONE':
                            return False
                        # else return True as path is clear!
                    return True

                if origin_y > destination_y:
                    # if origin is adjacent to empty destination then return True
                    if origin_y - 1 == destination_y:
                        return True
                    # check all squares between origin and destination from right to left
                    for col in range(origin_y - 1, destination_y, -1):
                        step = self.get_square_occupant(origin[0]+str(col))
                        # if there is another pawn in the way
                        if step != 'NONE':
                            return False
                        # else return True as path is clear!
                    return True

            if origin[1] == destination[1]:  # origin and destination are on same column

                # compare index of the row letters to determine if we're going up or down
                origin_x = self._row_letters.index(origin[0])
                destination_x = self._row_letters.index(destination[0])

                if origin_x < destination_x:
                    # if origin is adjacent to clear destination then return True
                    if origin_x + 1 == destination_x:
                        return True
                    # check all squares between origin and destination from top to bottom
                    for row_index in range(origin_x + 1, destination_x):
                        row_letter = self._row_letters[row_index]
                        step = self.get_square_occupant(row_letter + origin[1])
                        if step != 'NONE':
                            return False
                        # else return True as path is clear!
                    return True

                if origin_x > destination_x:
                    # if origin is adjacent to clear destination then return True
                    if origin_x - 1 == destination_x:
                        return True
                    # check all squares between origin and destination from bottom to top
                    for row_index in range(origin_x - 1, destination_x, -1):
                        row_letter = self._row_letters[row_index]
                        step = self.get_square_occupant(row_letter + origin[1])
                        if step != 'NONE':
                            return False
                        # else return True as path is clear!
                    return True
        # else
        return False

    def check_captures(self, position):
        """
        Method called by make_move to check if any captures are made by move. Checks if any pawns
        of opposing player are adjacent. If yes then checks what is on the opposite site of opposing pawn.
        If it is an empty square or off the board then return False. If it is a pawn belonging
        to the active player then return the position of the captured pawn to make_move.
        If two or more pawns of the opposing player are lined next to pawn then keep checking
        until there is either an empty square or board boundary or a pawn belonging to the active player.
        Also checks for corner captures by calling test_move on the active pawn and one perpendicular
        pawn belonging to the active player surrounding an enemy pawn. Tests movement towards nearest
        boundary by moving one square. If movement would take both off the board then corner capture
        is True.
        """
        # initialize a list to hold capture positions to send back to make_move
        capture_list = []

        # check for possible corner captures:
        corner_cap_positions = ['b1', 'a2', 'a8', 'b9', 'h9', 'i8', 'i2', 'h1']
        if position in corner_cap_positions:
            corner_cap = self.check_corner_capture(position)
            if corner_cap is not None:
                capture_list.append(corner_cap)

        # check to see if there are any adjacent pawns controlled by the opposing player
        pos_x = int(position[1])
        pos_y = self._row_letters.index(position[0])
        # initialize adjacent squares to "NONE"
        left_square = "NONE"
        right_square = "NONE"
        above_square = "NONE"
        bottom_square = "NONE"

        # check to see if we're on a border, in which case ignore that side
        # check to see if enemy pawn is left or right of pawn at position
        if pos_x != 1:
            left_square = self.get_square_occupant(position[0] + str(pos_x - 1))
        if pos_x != 9:
            right_square = self.get_square_occupant(position[0] + str(pos_x + 1))

        # check to see if enemy pawn is above or below pawn at position
        if pos_y != 0:
            prev_row = self._row_letters[pos_y - 1]
            above_square = self.get_square_occupant(prev_row + position[1])
        if pos_y != 8:
            next_row = self._row_letters[pos_y + 1]
            bottom_square = self.get_square_occupant(next_row + position[1])

        # if the square above the current position contains an enemy pawn
        if above_square != self.get_active_player() and above_square != "NONE":
            # initialize a temp list to add to capture_list
            above_captures = [(prev_row + position[1])]

            for y_pos in range(pos_y-2, -1, -1):
                row_letter = self._row_letters[y_pos]
                step = self.get_square_occupant(row_letter + position[1])
                # if there is no pawn on the other side then return
                if step == "NONE":
                    break
                # if there is a pawn belonging to active player on the opposite side
                if step == self.get_active_player():
                    # then add the captures to the capture list and check other sides
                    capture_list.extend(above_captures)
                    break
                # else keep going until there is either a capture or empty square
                above_captures.append((row_letter + position[1]))

        # if the square below the current position contains an enemy pawn
        if bottom_square != self.get_active_player() and bottom_square != "NONE":
            # initialize a temp list to add to capture_list
            bottom_captures = [(next_row + position[1])]

            for y_pos in range(pos_y + 2, 9):
                row_letter = self._row_letters[y_pos]
                step = self.get_square_occupant(row_letter + position[1])
                # if there is no pawn on the other side then return
                if step == "NONE":
                    break
                # if there is a pawn belonging to active player on the opposite side
                if step == self.get_active_player():
                    # then add the captures to the capture list and check other sides
                    capture_list.extend(bottom_captures)
                    break
                # else keep going until there is either a capture or empty square
                bottom_captures.append((row_letter + position[1]))

        # if the square to the left of the current position contains an enemy pawn
        if left_square != self.get_active_player() and left_square != "NONE":
            # initialize a temp list to add to capture_list
            left_captures = [(position[0] + str(pos_x - 1))]
            for x_pos in range(pos_x - 2, 0, -1):
                step = self.get_square_occupant(position[0] + str(x_pos))
                # if there is no pawn on the other side then return
                if step == "NONE":
                    break
                # if there is a pawn belonging to active player on the opposite side
                if step == self.get_active_player():
                    # then add the captures to the capture list and check other sides
                    capture_list.extend(left_captures)
                    break
                # else keep going until there is either a capture or empty square
                left_captures.append(position[0] + str(x_pos))

        # if the square to the right of the current position contains an enemy pawn
        if right_square != self.get_active_player() and right_square != "NONE":
            # initialize a temp list to add to capture_list
            right_captures = [(position[0] + str(pos_x + 1))]

            for x_pos in range(pos_x + 2, 10):
                step = self.get_square_occupant(position[0] + str(x_pos))
                # if there is no pawn on the other side then return
                if step == "NONE":
                    break
                # if there is a pawn belonging to active player on the opposite side
                if step == self.get_active_player():
                    # then add the captures to the capture list and check other sides
                    capture_list.extend(right_captures)
                    break
                # else keep going until there is either a capture or empty square
                right_captures.append(position[0] + str(x_pos))

        # return the capture_list and send to update_captures
        self.update_captures(self.get_active_player(), len(capture_list))
        return capture_list

    def check_corner_capture(self, position):
        """
        Method called by check_captures to check for possible corner captures.
        """
        # check top left corner
        if position == 'b1':
            if self.get_square_occupant('a2') == self.get_active_player():
                if self.get_square_occupant('a1') != (self.get_active_player() and "NONE"):
                    return 'a1'
        elif position == 'a2':
            if self.get_square_occupant('b1') == self.get_active_player():
                if self.get_square_occupant('a1') != (self.get_active_player() and "NONE"):
                    return 'a1'

        # check top right corner
        elif position == 'a8':
            if self.get_square_occupant('b9') == self.get_active_player():
                if self.get_square_occupant('a9') != (self.get_active_player() and "NONE"):
                    return 'a9'
        elif position == 'b9':
            if self.get_square_occupant('a8') == self.get_active_player():
                if self.get_square_occupant('a9') != (self.get_active_player() and "NONE"):
                    return 'a9'

        # check bottom right corner
        elif position == 'h9':
            if self.get_square_occupant('i8') == self.get_active_player():
                if self.get_square_occupant('i9') != (self.get_active_player() and "NONE"):
                    return 'i9'
        elif position == 'i8':
            if self.get_square_occupant('h9') == self.get_active_player():
                if self.get_square_occupant('i9') != (self.get_active_player() and "NONE"):
                    return 'i9'

        # check bottom left corner
        elif position == 'i2':
            if self.get_square_occupant('h1') == self.get_active_player():
                if self.get_square_occupant('i1') != (self.get_active_player() and "NONE"):
                    return 'i1'
        elif position == 'hi':
            if self.get_square_occupant('i2') == self.get_active_player():
                if self.get_square_occupant('i1') != (self.get_active_player() and "NONE"):
                    return 'i1'

    def update_captures(self, player, pawns_captured):
        """
        Method called by check_captures to update and track the number of captured
        pieces belonging to each player. Takes by argument which player lost the pieces and how many
        """
        if player == "RED":
            player = "BLACK"
        elif player == "BLACK":
            player = "RED"
        self._captured_pieces[player] += pawns_captured
        # call set_game_status to see if either player has won!
        self.set_game_status()

    def set_game_status(self):
        """
        If either player's pawn count reaches 1 then sets the game status to the x WON
        where x is the opposing player.
        """

        for player, pawns_captured in self._captured_pieces.items():
            if pawns_captured == 8:
                if player == "RED":
                    self._game_state = "BLACK WINS"
                if player == "BLACK":
                    self._game_state = "RED WINS"

    def update_turn(self):
        """
        Changes the active player/which player's turn it is following a legal move.
        """
        if self._active_player == "BLACK":
            self._active_player = "RED"
        else:
            self._active_player = "BLACK"

    def get_square_occupant(self, square):
        """
        Accepts a square position as an argument and returns either 'RED', 'BLACK' if occupied by
        either player or 'NONE' if square is unoccupied.
        """
        square_occupant = self._board.get(square)

        if square_occupant:
            if square_occupant == 'R':
                return "RED"
            elif square_occupant == 'B':
                return "BLACK"
            else:
                return "NONE"
        else:
            return "Invalid position: check algebraic notation"

    def print_board(self):
        """
        Prints the current state of the board. Board locations use algebraic notation and empty squares
        are represented by '.', black pawns are represented by 'B' and red pawns are represented by 'R'.
        """
        # hardcode the first row of numbers for algebraic notation
        first_row = "  1 2 3 4 5 6 7 8 9"
        print(first_row)

        for letter in self._row_letters:
            # initialize an empty string to hold the contents of each row
            row_string = letter
            for col_num in range(1, 10):
                val = self._board[letter + str(col_num)]
                row_string = row_string + ' ' + val

            print(row_string)
new_game = HasamiShogiGame()

