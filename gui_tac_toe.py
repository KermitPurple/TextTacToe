"""This module is a gui version of the module text_tac_toe"""

from text_tac_toe import TextTacToe, Coord, UserInput, InputType
import pygame, os

class GuiTacToe(TextTacToe):
    """
    This class uses pygame to create visual tic_tac_toe
    """

    def __init__(self, screen_size: Coord = Coord(600, 600)):
        super().__init__()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "15,30"
        self.running = False
        self.winner = None
        self.screen_size = screen_size
        pygame.display.init()
        pygame.display.set_caption('Tic Tac Toe')
        self.screen = pygame.display.set_mode(size=self.screen_size.get_tuple())

    def update(self):
        """
        called every frame
        update logic
        """
        self.winner = self.detect_winner()
        if self.winner is not None:
            self.running = False

    def print(self):
        """
        called every frame
        prints the screen
        """

    def play_game(self, player_x: InputType = UserInput, player_o: InputType = UserInput):
        """
        play a single game of tic tac toe
        """
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.screen.fill((0, 0, 0))
            self.update()
            pygame.display.update()
            print('a')
