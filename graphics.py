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

pygame.font.init()
main_font = pygame.font.SysFont('arial', 20)

class Graphics:
    """
    Class containing methods and attributes to create, update,
    and display the shogi game window and board using Pygame.
    """
    def __init__(self):
        self.screen = self.create_screen()
        self.board = self.create_board()
        self.restart = self.new_game_button()


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


        # draw the board including col and row nums and letters
        col_num = 9
        row_index = 0

        for x in range(0, WIN_WIDTH, SQUARE_SIZE):
            for y in range(0, BOARD_HEIGHT, SQUARE_SIZE):

                rect = pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE)
                # render the column numbers

                if y == 0 and x > 0 and col_num > 0:
                    col_rect = pygame.Rect(x + 10, 10, SQUARE_SIZE, 0)
                    col_text = main_font.render(str(col_num), True, (0, 0, 0))
                    self.screen.blit(col_text, col_rect)
                    # decrement col num
                    col_num = int(col_num) - 1

                # render the row letters
                if y > 0 and x > BOARD_WIDTH:
                    row_rect = pygame.Rect(WIN_WIDTH - 25, y, SQUARE_SIZE, 0)
                    row_text = main_font.render(ROW_LETTERS[row_index], True, (0, 0, 0))
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

    def draw(self, pieces, turn):
        """
        Render the current board state
        """

        # clear area where the player turn text is displayed
        status_rect = pygame.Rect( (BOARD_WIDTH - SQUARE_SIZE),
                                  WIN_HEIGHT - 35, (SQUARE_SIZE * 3), 30)
        self.screen.fill((255, 255, 255), status_rect)

        # draw  player turn status text in the cleared area
        status_text = main_font.render(str(turn + "\'s turn"), True, (turn))
        self.screen.blit(status_text, status_rect)

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
        If one exists then return piece.
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
            rect = pygame.Rect(pos[0] * SQUARE_SIZE + 2, 
                               pos[1] * SQUARE_SIZE + 2, SQUARE_SIZE - 4, SQUARE_SIZE - 4)
            self.board.fill(HIGHLIGHT_COLOR, rect)
            self.screen.blit(self.board, (50, 50))

    def new_game_button(self):
        """
        Draws a New Game button onto the screen.
        """

        button_font = pygame.font.SysFont('arial', 15)

        text = button_font.render("New Game", True, "BLACK")
        rect = pygame.Rect(50, WIN_HEIGHT - 35, (SQUARE_SIZE * 1.5), 30)
        # draw the button outline

        pygame.draw.rect(self.screen, "BLACK", rect, 1)
        # get the rect of the text and center it in the button rect
        text_rect = text.get_rect(center=rect.center)

        self.screen.blit(text, text_rect)
        # return the new game rect to the constructor to check for presses later
        return rect

    def button_press(self, pos):
        """
        Checks for button presses -
        Currently only has one (new game) button
        """
        return self.restart.collidepoint(pos)



    def display_game_over(self, winner):
        """
        Displays a game over message on the screen including
        the winner's name.
        """

        # Set up font and message
        font = pygame.font.SysFont('arial', 75, bold=True)
        game_over_text = "Game Over"
        winner_text = f"{winner} Wins!"

        # Render the messages
        game_over_surface = font.render(game_over_text, True, (255, 180, 0)) # nice gold color

        game_over_shadow = font.render(game_over_text, True, (0, 0, 0))      # black shadow

        winner_surface = font.render(winner_text, True, (winner))            # use the winning color

        # Calculate positions for centered text
        game_over_rect = game_over_surface.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 - 50))
        winner_rect = winner_surface.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 30))

        # Blit the messages onto the screen

        self.screen.blit(game_over_shadow, (game_over_rect.x - 3, game_over_rect.y - 3))
        self.screen.blit(game_over_surface, game_over_rect)
        self.screen.blit(winner_surface, winner_rect)




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
        piece_png = pygame.image.load(f"pieces/{self.color.lower()}_piece.png")

        # red pieces should be rotated 180 degrees as though they are facing opposite player
        if self.color == "RED":
            piece_png = pygame.transform.rotate(piece_png, 180)

        # scale the piece pngs using the square size based on the set board resolution
        piece_png = pygame.transform.smoothscale(piece_png, (SQUARE_SIZE, SQUARE_SIZE))

        surface.blit(piece_png, (self.x * SQUARE_SIZE, self.y * SQUARE_SIZE))
