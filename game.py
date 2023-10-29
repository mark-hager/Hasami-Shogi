"""
Contains classes and methods for creating a new game of Hasami Shogi
"""

import pygame

import graphics

class Game:
    """
    An instance of Hasami Shogi.
    Initializes the game window and represents game state information
    using Pygame by calling functions from graphics.py. 
    Also importing shogi_var1.py for game logic and rules 

    with help from Michael Maranan's Pygame Checkers tutorial:
    https://thepythoncode.com/article/make-a-checkers-game-with-pygame-in-python
    """
    # constants
    ROWS = 9
    COLS = 9

    def __init__(self):
        # initialize the window and the game board.
        # window size is currently defined in graphics.py but may make dynamic later
        self.graphics = graphics.Graphics()

        # track the board state using a dictionary
        # pawns are recorded using xy coords as keys in a tuple
        self.board = self.create_board()
        # initialize player turn to black as they always start
        self._active_player = "BLACK"
        # initialize dictionary to hold how many pieces lost by each player
        self._pieces_remaining = {
                                  "BLACK": 9,
                                  "RED": 9,
                                 }
        self._selected_piece = None
        # initialize the new game as unfinished
        self.running = True
        # draw the pieces onto the board
        self.graphics.draw(self.board)
        self.FPS = pygame.time.Clock()


    def create_board(self):
        """
        Create the game board using a dictionary. The keys of each item are
        a tuple representing coordinates on the board such that the first item key is (0, 0).
        The value of each item represents whether that square is occupied by either
        color of pawn or is unoccupied.
        """
        # create a new dictionary to hold the squares
        new_board = {}
        # list of the row letters to iterate through
        for y in range (self.ROWS):
            for x in range (self.COLS):
                # fill the top row with Red pawns
                if y == 0:
                    new_board[ (x, y) ] = 'RED'
                # fill the bottom row with Black pawns
                elif y == 8:
                    new_board[ (x, y) ] = 'BLACK'
                # the rest of the board starts empty
                #else:
                #    new_board[ (x, y) ] = '.'

        return new_board



    def test_move(self, origin):
        """
        Ensures that a given move is legal by checking that destination
        is either horizontal or vertical to origin. Also checks to make sure there is no 
        collision with other pieces. Returns True if move is legal, else returns False
        """
        # set to hold all possible moves from origin square. pawns can move horizontally
        # or vertically like rooks. pawns cannot jump other pawns
        legal_moves = set()

        x, y = origin

        # check horizontal spaces, first by checking to the right of origin

        if x < self.COLS - 1:
            for col in range(x + 1, self.COLS):
                if not self.board.get( (col, y) ):
                    legal_moves.add( (col, y) )
                else:
                    break
        # then look to the left
        if x > 0:
            for col in range(x - 1, -1, -1):
                if not self.board.get( (col, y) ):
                    legal_moves.add( (col, y) )
                else:
                    break
        # check vertical spaces starting with squares below origin
        if y < self.ROWS - 1:
            for row in range(y + 1, self.ROWS):
                if not self.board.get( (x, row) ):
                    legal_moves.add( (x, row ))
                else:
                    break
        # then look at squares above origin
        if y > 0:
            for row in range(y - 1, -1, -1):
                if not self.board.get( (x, row) ):
                    legal_moves.add( (x, row) )
                else:
                    break

        return legal_moves


    def check_captures(self, pos):
        """
        Method called by make_move to check if any captures
        are made by move.
        If any pawns
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

        # get the opposing player
        if self._active_player == "BLACK":
            opponent = "RED"
        else:
            opponent = "BLACK"
     
        x, y = pos
        # check for special corner captures - separate method needed?

        # these need to check for n < 8 pieces being captured, not just one
        
        # represents number of pieces to get captured, max = 7


        # check for captures above piece
        if y > 1:
            n = 1
            temp_caps = []
            while self.board.get( (x, y - n) ) == opponent:
                temp_caps.append( (x, y - n) )
                n += 1
                
            if n > 1:
                if self.board.get( (x, y - n) ) == self._active_player:
                    for piece in temp_caps:
                        capture_list.append(piece)

        # check for captures below piece
        if y < self.ROWS - 2:
            n = 1
            temp_caps = []
            while self.board.get( (x, y + n) ) == opponent:
                temp_caps.append( (x, y + n) ) 
                n += 1
            if n > 1:
                if self.board.get( (x, y + n) ) == self._active_player:
                    for piece in temp_caps:
                        capture_list.append(piece)


        # check for captures left of piece
        if x > 1:
            n = 1
            temp_caps = []
            while self.board.get( (x - n, y) ) == opponent:
                temp_caps.append( (x - n, y) )
                n += 1
                
            if n > 1:
                if self.board.get( (x - n, y) ) == self._active_player:
                    for piece in temp_caps:
                        capture_list.append(piece)

        # check for captures right of piece
        if x < self.COLS - 2:
            n = 1
            temp_caps = []
            while self.board.get( (x + n, y) ) == opponent:
                temp_caps.append( ( x + n, y) )
                n += 1
            if n > 1:
                if self.board.get( (x + n, y) ) == self._active_player:
                    for piece in temp_caps:
                        capture_list.append(piece)
        

        return capture_list


    def make_move(self, origin, destination):
        """
        Moves the active player's selected piece.
        Updates the board
        *TODO* check for captures or in separate method?
        """
        print("Selected piece: " + str(origin))
        # update the board: copy the piece to the clicked square,
        self.board[ (destination) ] = self._active_player
        # remove it from its origin,
        del self.board[ (origin) ]
        #self.board[ (origin) ] = '.'

        # checking if the move makes any captures
        cap_list = self.check_captures(destination)

        # remove captured pieces from the board
        for piece in cap_list:
            print(piece)
            # record whether the captured piece was black or red
            if self.board[piece] == "BLACK":
                self._pieces_remaining["BLACK"] -= 1
                print("BLACK PIECE CAPTURED!")
            else:
                self._pieces_remaining["RED"] -= 1
                print("RED PIECE CAPTURED!")

            # and delete the captured piece from the game board
            del self.board[ (piece) ]
            
            #*TODO* logic that ends game if pieces remaining == 1
        # and redraw the shogi board
        self.graphics.draw(self.board)

        # switch the active player following a legal move
        self.update_turn()


    def update_turn(self):
        """
        Flips the active player depending on whether it's RED or BLACKs turn
        following a legal move.
        """
        if self._active_player == "BLACK":
            self._active_player = "RED"
        else:
            self._active_player = "BLACK"


    def main_loop(self):
        """
        main game loop
        """
        while self.running is True:

            #game.check_move(display)

            for self.event in pygame.event.get():

                if self.event.type == pygame.QUIT:
                    self.running = False

                    pygame.quit()
                    sys.exit()

                #if ShogiVar1.get_game_state() != 'UNFINISHED':
                if self.event.type == pygame.MOUSEBUTTONDOWN:
                    # get the position of the click
                    mouse_pos = pygame.mouse.get_pos()
                    # and check that occupant at position matches player whose turn it is
                    clicked_square = self.graphics.get_occupant(mouse_pos)

                    # check that clicked square contains piece belonging to active player
                    if self.board.get(clicked_square) == self._active_player:

                        self._selected_piece = clicked_square
                        # refresh the board/clear any existing highlights
                        self.graphics.draw(self.board)
                        # show all available moves from origin
                        possible_moves = self.test_move(self._selected_piece)
                        # highlight the squares that the selected piece can legally move to
                        self.graphics.highlight_square(possible_moves)

                    # also check if clicked square is a legal move for the selected piece.
                    elif self._selected_piece and clicked_square in possible_moves:
                        # call make move method
                        self.make_move(self._selected_piece, clicked_square)
                        # reset the selected piece and move set once the move is made
                        self._selected_piece = None
                        possible_moves = None

              #  else:
                    #game.message()
                  #  self.running = False

            # redraw the pygame board
            #self.graphics.draw(self.board)
            pygame.display.update()
            self.FPS.tick(30)


if __name__ == "__main__":

    new_game = Game()
    new_game.main_loop()
