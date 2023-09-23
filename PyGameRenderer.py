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
from shogi_var1 import *

# constants, but may experiment with enabling scaling in an options menu

WIN_WIDTH, WIN_HEIGHT = 750, 750
# Hasami Shogi boardsize is 9x9
ROWS, COLS = 9, 9
# board is a surface that is blit'd onto screen
BOARD_WIDTH, BOARD_HEIGHT = (WIN_WIDTH - 100), (WIN_HEIGHT - 100)
# height and width of each individual square,
# floor division is making board tiling wonky depending on screen size
SQUARE_SIZE = BOARD_WIDTH // COLS
# board letters
row_letters = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i')

pygame.init()


# set up the window
size = (WIN_WIDTH , WIN_HEIGHT)
screen = pygame.display.set_mode(size)
screen.fill("WHITE")
pygame.display.set_caption("Hasami Shogi")


# set up the board
board = pygame.Surface((BOARD_WIDTH, BOARD_HEIGHT))
board.fill((250, 250, 180))


# render the rows and column coordinates
pygame.font.init()
my_font = pygame.font.SysFont('arial', 20)



# draw the board including col and row numbs and letters
col_num = 9
row_letters = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i')
row_index = 0

for x in range(0, WIN_WIDTH, SQUARE_SIZE):
    for y in range(0, BOARD_HEIGHT, SQUARE_SIZE):

        rect = pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE)
        # render the column numbers
        if y == 0 and x > 0 and col_num > 0:
            col_rect = pygame.Rect(x + 10, 10, SQUARE_SIZE, 0)
            col_text = my_font.render(str(col_num), True, (0, 0, 0))
            screen.blit(col_text, col_rect)
            # decrement col num
            col_num = int(col_num) - 1

        # render the row letters
        if y > 0 and x > BOARD_WIDTH:
            row_rect = pygame.Rect(WIN_WIDTH - 25, y, SQUARE_SIZE, 0)
            row_text = my_font.render(row_letters[row_index], True, (0, 0, 0))
            screen.blit(row_text, row_rect)
            # increment the row index to get the next letter
            row_index += 1

        pygame.draw.rect(board, "BLACK", rect, 1)


# draw a black square around the game board because it looks nice
border = pygame.Rect(40, 40, BOARD_WIDTH + 18, BOARD_HEIGHT + 18)
pygame.draw.rect(screen, "BLACK", border, 1)


# add the board to the screen
screen.blit(board, (50, 50))

class Piece:
    """
    Represents individual shogi pieces on the game board.
    """
    def __init__(self, color, x, y, piece_type):
        self.color = color
        self.x = x
        self.y = y
        self.type = piece_type

    def draw(self, surface):
        """
        draw the piece and place it in the middle of its square
        width of 0 makes it filled
        """

        piece_png = pygame.image.load(f"pieces/{self.color.lower()}_piece.png")

        # red pieces should be rotated 180 degrees as though they are facing opposite player
        if self.color == "RED":
            piece_png = pygame.transform.rotate(piece_png, 180)

        # scale the piece pngs using the square size based on the set board resolution
        piece_png = pygame.transform.smoothscale(piece_png, (SQUARE_SIZE, SQUARE_SIZE))

        surface.blit(piece_png, (self.x * SQUARE_SIZE, self.y * SQUARE_SIZE))

# set up the pieces
pieces = []
for i in range(COLS):
    pieces.append(Piece("RED", i, 0, "pawn"))
    pieces.append(Piece("BLACK", i, 8, "pawn"))

# draw the pieces
for piece in pieces:
    piece.draw(board)
screen.blit(board, (50, 50))

pygame.display.flip()

# main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # get the position of the click
            pos = pygame.mouse.get_pos()
            x_coord = (pos[0] - 50) // SQUARE_SIZE
            print(pos)
            # invert the x coordinate since col 0 is actually col 9 on the board
            print("X coordinate is: ", x_coord)
            y_coord = (pos[1] - 50) // SQUARE_SIZE
            if y_coord >= 0 and y_coord < 9:
                print("Y coordinate is: ", row_letters[y_coord])
            
                        # find the piece at the clicked position
            for piece in pieces:

                if piece.x == x_coord and piece.y == y_coord:
                    print("Piece here!")