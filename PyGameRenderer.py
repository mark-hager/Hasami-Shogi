"""
Contains methods for rendering the Shogi game
using Pygame.
With help from Everest Whitman's lovely checkers pygame implementation:
https://github.com/everestwitman/Pygame-Checkers/blob/master/checkers.py
"""
import pygame


class RenderGame:
    """
    Renders the Shogi game passed to it. Contains 
    methods for displaying the game board, pawns
    and misc. information like whose turn it is
    and the number of pawns captured by each player.

    """
    def __init__(self):
        """
        Initializes the Pygame renderer.
        """
        self.caption = "Hasami Shogi"
        pygame.display.set_caption(self.caption)

        self.clock = pygame.time.Clock()
        # set the frame rate
        self.clock.tick(30) 

        self.win_width = 600
        self.win_height = 600
        # set the window dimensions
        self.screen = pygame.display.set_mode((self.win_width, self.win_height))
        
        self.square_size = self.win_width / 9
        self.piece_size = self.square_size / 2

        # initialize the pygame window
        pygame.init()
        self.render_board()
        self.game_loop()
    
    def render_board(self):
        """
        Renders the squares of the board
        """
        for x in range(9):
            for y in range(9):
                pygame.draw.rect(self.screen, "purple", 
                                (x * self.square_size, y * self.square_size, 
                                self.square_size, self.square_size), )


    def game_loop(self):
        """
        Runs the main loop
        """

        while True:
            # Process player inputs.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit

            # Do logical updates here.
            # ...

            #self.screen.fill("purple")  # Fill the display with a solid color

            # Render the graphics here.
            # ...

            #pygame.display.flip()  # Refresh on-screen display

            self.clock.tick(60)         # wait until next frame (at 60 FPS)