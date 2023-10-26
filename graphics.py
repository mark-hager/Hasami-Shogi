"""
Contains methods for rendering the Shogi game
using Pygame.
With help from Tech With Jim's lovely checkers pygame implementation:
https://www.youtube.com/watch?v=vnd3RfeG3NM
Also used Arslan Mirza's Chess pygame tutorial:
https://medium.com/javarevisited/how-to-build-a-chess-game-with-pygame-in-python-9eb0a7591776
"""
import sys
import pygame

# constants, but may experiment with enabling scaling in an options menu

WIN_WIDTH, WIN_HEIGHT = 750, 750
# Hasami Shogi boardsize is 9x9
ROWS, COLS = 9, 9
# board is a surface that is blit'd onto screen
BOARD_WIDTH, BOARD_HEIGHT = (WIN_WIDTH - 100), (WIN_HEIGHT - 100)
# height and width of each individual square,
# floor division is making board tiling wonky depending on screen size
HIGHLIGHT_COLOR = (100, 250, 90)
SQUARE_SIZE = BOARD_WIDTH // COLS
# board letters
ROW_LETTERS = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i')


pygame.init()

class Graphics:
    """
    Class containing methods and attributes to create, update,
    and display the shogi game window and board using Pygame.
    """
    def __init__(self):
        self.screen = self.create_screen()
        self.board = self.create_board()


    def create_screen(self):
        """
        Initialize the Pygame screen
        """
        size = (WIN_WIDTH , WIN_HEIGHT)
        screen = pygame.display.set_mode(size)
        screen.fill("WHITE")
        pygame.display.set_caption("Hasami Shogi")
        
        return screen

    def create_board(self):

        """
        Initialize the game board
        """
        # set up the board
        board = pygame.Surface((BOARD_WIDTH, BOARD_HEIGHT))
        board.fill((250, 250, 180))

        # render the rows and column coordinates
        pygame.font.init()
        my_font = pygame.font.SysFont('arial', 20)

        # draw the board including col and row nums and letters
        col_num = 9
        row_index = 0

        for x in range(0, WIN_WIDTH, SQUARE_SIZE):
            for y in range(0, BOARD_HEIGHT, SQUARE_SIZE):

                rect = pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE)
                # render the column numbers
                
                if y == 0 and x > 0 and col_num > 0:
                    col_rect = pygame.Rect(x + 10, 10, SQUARE_SIZE, 0)
                    col_text = my_font.render(str(col_num), True, (0, 0, 0))
                    self.screen.blit(col_text, col_rect)
                    # decrement col num
                    col_num = int(col_num) - 1

                # render the row letters
                if y > 0 and x > BOARD_WIDTH:
                    row_rect = pygame.Rect(WIN_WIDTH - 25, y, SQUARE_SIZE, 0)
                    row_text = my_font.render(ROW_LETTERS[row_index], True, (0, 0, 0))
                    self.screen.blit(row_text, row_rect)
                    # increment the row index to get the next letter
                    row_index += 1

                pygame.draw.rect(board, "BLACK", rect, 1)

        # draw a black square around the game board because it looks nice
        border = pygame.Rect(40, 40, BOARD_WIDTH + 18, BOARD_HEIGHT + 18)
        pygame.draw.rect(self.screen, "BLACK", border, 1)

        # add the board to the screen
        self.screen.blit(board, (50, 50))

        return board
    
    def draw(self, pieces):
        """
        Render the current board state
        """

        # redraw the board only

        self.board.fill((250, 250, 180))
        
        for x in range(0, WIN_WIDTH, SQUARE_SIZE):
            for y in range(0, BOARD_HEIGHT, SQUARE_SIZE):

                rect = pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE)

                pygame.draw.rect(self.board, "BLACK", rect, 1)

        # go through the board dictionary and find any pieces
        for y in range (ROWS):
            for x in range (COLS):
                # if piece exists at coord
                if pieces.get( (x, y )) == 'BLACK':
                    piece = Piece("BLACK", x, y, "pawn")
                    # then draw it onto the board
                    piece.draw(self.board)

                elif pieces.get( (x, y )) == 'RED':
                    piece = Piece("RED", x, y, "pawn")
                    piece.draw(self.board)
        

        self.screen.blit(self.board, (50, 50))


    def get_occupant(self, pos):
        """
        Check if piece exists at the coordinates from the mouseclick event.
        If exits then return piece.
        """

        row = (pos[0] - 50) // SQUARE_SIZE

        column = (pos[1] - 50) // SQUARE_SIZE

        # reversed x and y since board is 2d array of rows of columns
        # piece = pieces.get( (y_square, x_square ))
        return (row, column)

    # def highlight_square(self, squares)
    # takes a list of tuples containing coordinates of squares to be highlighted.
    def highlight_square(self, squares):
        """
        Highlights squares on the board to indicate selected piece
        and possible moves.
        """
        for pos in squares:
            # hacky math is to account for borders; does not scale. bad solution
            rect = pygame.Rect(pos[0] * SQUARE_SIZE + 2, pos[1] * SQUARE_SIZE + 2, SQUARE_SIZE - 4, SQUARE_SIZE - 4)
            self.board.fill(HIGHLIGHT_COLOR, rect)
            self.screen.blit(self.board, (50, 50))



class Piece:
    """
    Represents individual shogi pieces on the game board.
    """
    def __init__(self, color, x, y, piece_type):
        self.color = color
        self.x = x
        self.y = y
        self.type = piece_type
        # defaults to False; only true when piece is clicked
        self.selected = False

    def draw(self, surface):
        """
        draw the piece and place it in the middle of its square
        width of 0 makes it filled
        """

        #if self.selected is False:
          #  rect = pygame.Rect(self.x * SQUARE_SIZE, self.y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
          #  surface.fill(HIGHLIGHT_COLOR, rect)
            #pygame.draw.rect(self.board, HIGHLIGHT_COLOR, SQUARE_SIZE) 

        piece_png = pygame.image.load(f"pieces/{self.color.lower()}_piece.png")

        # red pieces should be rotated 180 degrees as though they are facing opposite player
        if self.color == "RED":
            piece_png = pygame.transform.rotate(piece_png, 180)

        # scale the piece pngs using the square size based on the set board resolution
        piece_png = pygame.transform.smoothscale(piece_png, (SQUARE_SIZE, SQUARE_SIZE))

        surface.blit(piece_png, (self.x * SQUARE_SIZE, self.y * SQUARE_SIZE))

