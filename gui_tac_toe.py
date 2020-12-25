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
    GREEN = pygame.Color(0, 255, 0)
    BLUE = pygame.Color(0, 0, 255)
    MAX_TIKS = 1000000
    tiks_at_game_over = 0

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
        self.game_over = False

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
        self.print()
        if not self.game_over:
            self.player = self.player_x if self.current_turn == Team.X else self.player_o
            self.winner = self.detect_winner()
            if self.winner is not None:
                self.game_over = True
                self.tiks_at_game_over = self.tiks
            elif (pos := self.player.get_input(self)) is not None:
                self.set_board(pos)
        else:
            self.draw_game_over_screen()
            if self.tiks > self.tiks_at_game_over + 40:
                self.reset()

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
            pygame.draw.line(self.screen, self.RED, pos.get_tuple(), Coord(pos.x + scaled_cell_size.x, pos.y + scaled_cell_size.y).get_tuple(), 10)
            pygame.draw.line(self.screen, self.RED, Coord(pos.x, pos.y + scaled_cell_size.y).get_tuple(), Coord(pos.x + scaled_cell_size.x, pos.y).get_tuple(), 10)
        elif team == Team.O:
            middle = Coord(pos.x * self.cell_size.x + self.cell_size.x / 2, pos.y * self.cell_size.y + self.cell_size.y / 2)
            pygame.draw.circle(self.screen, self.GREEN, middle.get_tuple(), min(self.cell_size.x, self.cell_size.y) * 0.4, 10)

    def draw_text(self, pos: Coord, text: str, color: pygame.Color):
        """
        Draws text to the screen
        """
        txt = self.FONT.render(text, True, color)
        size = txt.get_size()
        self.screen.blit(txt, Coord(pos.x - size[0] / 2, pos.y).get_tuple())

    def draw_game_over_screen(self):
        """
        Draw the text on the screen for when the game ends
        """
        center = Coord(self.screen_size.x / 2, self.screen_size.y / 2)
        top_center = Coord(center.x, self.screen_size.y * 0.2)
        x_offset = self.screen_size.x / 4
        if self.winner == Team.Empty:
            color = self.BLUE
            text = 'Cat\'s Game!'
        else:
            text = f'{self.winner.value} Won!'
            if self.winner == Team.X:
                color = self.RED
            else:
                color = self.GREEN
        self.draw_text(top_center, text, color)
        self.draw_text(Coord(center.x - x_offset, center.y), f'X: {0}', self.RED)
        self.draw_text(Coord(center.x + x_offset, center.y), f'O: {0}', self.GREEN)

    def mouse_input(self, pos, button):
        """
        get the mouse input
        """
        if button == 1:
            if self.game_over:
                self.reset()
            elif self.player == PygameUserInput:
                grid_pos = Coord(int(pos[0] / self.cell_size.x), int(pos[1] / self.cell_size.y))
                self.set_board(grid_pos)

    def reset(self):
        """
        Reset the board, current turn, and tiks
        """
        super().reset()
        self.game_over = False
        tiks = 0

    def play_game(self):
        """
        play a single game of tic tac toe
        """
        self.running = True
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

