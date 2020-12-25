"""This module is a gui version of the module text_tac_toe"""

from text_tac_toe import TextTacToe, Coord, UserInput, InputType, Team
import pygame, os, time, sys

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
    RED = pygame.Color(255, 0, 0)
    MAX_TIKS = 1000000

    def __init__(self, player_x: InputType = PygameUserInput, player_o: InputType = PygameUserInput, board_size: Coord = Coord(3, 3), screen_size: Coord = Coord(600, 600)):
        super().__init__(player_x, player_o, board_size)
        os.environ['SDL_VIDEO_WINDOW_POS'] = "15,30"
        self.running = False
        self.winner = None
        self.cell_size = Coord(screen_size.x / self.board_size.x, screen_size.y / self.board_size.y)
        self.screen_size = screen_size
        pygame.font.init()
        pygame.display.init()
        pygame.display.set_caption('Tic Tac Toe')
        self.FONT = pygame.font.SysFont('Arial', 100)
        self.screen = pygame.display.set_mode(size=self.screen_size.get_tuple())
        self.tiks = 0
        self.showing_winner = False

    def tik(self):
        """
        increment tiks and sleep for 0.05 seconds
        """
        self.tiks += 1
        self.tiks %= self.MAX_TIKS
        time.sleep(0.05)

    def update(self):
        """
        called every frame
        update logic
        """
        self.player = self.player_x if self.current_turn == Team.X else self.player_o
        self.winner = self.detect_winner()
        if self.winner is not None:
            self.reset()
            self.showing_winner = True
            self.tiks_at_show_win = self.tiks
        if (pos := self.player.get_input(self)) is not None:
            self.set_board(pos)
        self.print()
        if self.showing_winner:
            self.draw_winner()
            if self.tiks > self.tiks_at_game_over + 40:
                self.showing_winner = False

    def set_board(self, pos: Coord):
        """
        set a position on the board to the current turn
        """
        try:
            if pos.x >= self.board_size.x or pos.x < 0 or pos.y >= self.board_size.y or pos.y < 0:
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
        for i in range(self.board_size.y):
            for j in range(self.board_size.x):
                self.draw_cell(Coord(j, i), self.board[i][j])

    def draw_grid(self):
        """
        Draw the tic tac toe grid
        """
        for i in range(1, self.board_size.x):
            pygame.draw.line(self.screen, self.WHITE, (i * self.cell_size.x, 0), (i * self.cell_size.x, self.screen_size.y))
        for i in range(1, self.board_size.y):
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

    def draw_winner(self):
        center = Coord(self.screen_size.x / 2, self.screen_size.y / 2)
        txt = self.FONT.render('Test', True, self.RED)
        self.screen.blit(txt, center.get_tuple())

    def mouse_input(self, pos, button):
        """
        get the mouse input
        """
        if self.player == PygameUserInput and button == 1:
            grid_pos = Coord(int(pos[0] / self.cell_size.x), int(pos[1] / self.cell_size.y))
            self.set_board(grid_pos)

    def reset(self):
        """
        Reset the board, current turn, and tiks
        """
        super().reset()
        tiks = 0

    def play_game(self):
        """
        play a single game of tic tac toe
        """
        while self.running:
            self.tik()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_input(event.pos, event.button)
            self.screen.fill(self.BLACK)
            self.update()
            pygame.display.update()

