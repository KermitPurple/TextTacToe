"""This module is a gui version of the module text_tac_toe"""

from text_tac_toe import TextTacToe, Coord, UserInput, InputType, Team
import pygame, os

class PygameUserInput(InputType):
    """
    Child class of Input type.
    Read user input from pygame mouse
    """

    @staticmethod
    def get_input(tic_tac_toe: TextTacToe) -> Coord:
        """
        Returns none because the user input is found in the pygame loops
        """
        return None

class GuiTacToe(TextTacToe):
    """
    This class uses pygame to create visual tic_tac_toe
    """

    WHITE = pygame.Color(255, 255, 255)
    BLACK = pygame.Color(0, 0, 0)

    def __init__(self, screen_size: Coord = Coord(600, 600)):
        super().__init__()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "15,30"
        self.running = False
        self.winner = None
        self.cell_size = Coord(screen_size.x / self.size.x, screen_size.y / self.size.y)
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
        if (pos := self.player.get_input(self)) is not None:
            self.set_board(pos)
        self.print()

    def set_board(self, pos: Coord):
        """
        set a position on the board to the current turn
        """
        try:
            if pos.x >= self.size.x or pos.x < 0 or pos.y >= self.size.y or pos.y < 0:
                raise ValueError('Coordinate out of bounds')
            if self.board[pos.y][pos.x] != Team.Empty:
                raise ValueError('Cannot place peice in spot that isnt empty')
            self.board[pos.y][pos.x] = self.current_turn
            self.swap_current_turn()
        except ValueError as error:
            print(error)

    def print(self):
        """
        prints the screen
        """
        self.draw_grid()
        for i in range(self.size.y):
            for j in range(self.size.x):
                self.draw_cell(Coord(j, i), self.board[i][j])

    def draw_grid(self):
        """
        Draw the tic tac toe grid
        """
        for i in range(1, self.size.x):
            pygame.draw.line(self.screen, self.WHITE, (i * self.cell_size.x, 0), (i * self.cell_size.y, self.screen_size.y))
        for i in range(1, self.size.y):
            pygame.draw.line(self.screen, self.WHITE, (0, i * self.cell_size.y), (self.screen_size.x, i * self.cell_size.y))

    def draw_cell(self, pos: Coord, team: Team):
        """
        Fill a cell with an x or an o
        """
        if team  == Team.X:
            pos = Coord(pos.x * self.cell_size.x + self.cell_size.x * 0.1, pos.y * self.cell_size.y + self.cell_size.x * 0.1)
            scaled_cell_size = Coord(self.cell_size.x * 0.8, self.cell_size.y * 0.8)
            pygame.draw.line(self.screen, self.WHITE, pos.get_tuple(), Coord(pos.x + scaled_cell_size.x, pos.y + scaled_cell_size.y).get_tuple(), 10)
            pygame.draw.line(self.screen, self.WHITE, Coord(pos.x, pos.y + scaled_cell_size.y).get_tuple(), Coord(pos.x + scaled_cell_size.x, pos.y).get_tuple(), 10)
        elif team == Team.O:
            middle = Coord(pos.x * self.cell_size.x + self.cell_size.x / 2, pos.y * self.cell_size.y + self.cell_size.y / 2)
            pygame.draw.circle(self.screen, self.WHITE, middle.get_tuple(), min(self.cell_size.x, self.cell_size.y) * 0.4, 10)

    def mouse_input(self, pos, button):
        """
        get the mouse input
        """
        if button == 1:
            grid_pos = Coord(int(pos[0] / self.cell_size.x), int(pos[1] / self.cell_size.y))
            self.set_board(grid_pos)

    def play_game(self, player_x: InputType = PygameUserInput, player_o: InputType = PygameUserInput):
        """
        play a single game of tic tac toe
        """
        self.player = player_x if self.current_turn == Team.X else player_o
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_input(event.pos, event.button)
            self.screen.fill((0, 0, 0))
            self.update()
            pygame.display.update()
