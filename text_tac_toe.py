"""Contains five classes used for a text-based TicTacToe game"""

from __future__ import annotations # allows for use of Coord in function type declarations
from enum import Enum
import random


class Team(Enum):
    """
    A enum containing the two types of teams in tic tac toe
    """
    X = 'X'
    O = 'O'
    Empty = ' '

class Coord:
    """
    a representation of an x and y coordinate
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_tuple(self):
        """
        Coord it as a tuple
        """
        return self.x, self.y

    @staticmethod
    def from_string(string: str) -> Coord:
        """
        Create a new Coord object from a string
        """
        # split input string into list of empy strings and numbers
        num_list = (''.join(map(lambda ch: ch if ch.isnumeric() else ' ', string))).split(' ')
        while '' in num_list: # While there are empty strings
            num_list.remove('') # remove an empty string
        length = len(num_list)
        if length < 2:
            raise ValueError('Not enough numbers for a coordinate in a 2d plane')
        if length > 2:
            raise ValueError('Too many numbers for a coordinate in a 2d plane')
        return Coord(int(num_list[0]), int(num_list[1]))

    def __eq__(self, other: Coord) -> bool:
        """
        Compare two Coord objects with a double equals operator
        """
        return self.x == other.x and self.y == other.y

    def __str__(self) -> str:
        """
        Return the Coord object as a tstring
        """
        return f'Coord(x={self.x}, y={self.y})'

class InputType:
    """
    A class to be inherited and used to define the types of input that can be used for tic tac toe
    some examples of input types would be user or bot
    used in TextTacToe for get_input method
    """

    @staticmethod
    def get_input(tic_tac_toe: TextTacToe) -> Coord:
        """
        The method that should be overwritten and is used in TextTacToe
        """
        return Coord(0, 0)

class UserInput(InputType):
    """
    Child class of Input type.
    Asks the user to enter input and returns it as a coord
    """

    @staticmethod
    def get_input(tic_tac_toe: TextTacToe) -> Coord:
        """
        get user input and covert it to a Coord
        """
        return Coord.from_string(input('Enter a valid Coordinate on the board: '))

class RandomBotInput(InputType):
    """
    Child class of Input type.
    returns a random avaliable coord on the board
    """

    @staticmethod
    def get_avaliable_coords(tic_tac_toe: TextTacToe, board: [[Team]]) -> [Coord]:
        """
        Return a list of avaliable coordinates
        """
        avaliable_coords = []
        for i in range(tic_tac_toe.board_size.y):
            for j in range(tic_tac_toe.board_size.x):
                if board[i][j] == Team.Empty:
                    avaliable_coords.append(Coord(j, i))
        return avaliable_coords

    @staticmethod
    def get_input(tic_tac_toe: TextTacToe) -> Coord:
        """
        get user input and covert it to a Coord
        """
        return random.choice(RandomBotInput.get_avaliable_coords(tic_tac_toe, tic_tac_toe.board))

class MinimaxBotInput(RandomBotInput):
    """
    Child class of Input type.
    computes what the best move should be using minimax algorithm
    """

    @staticmethod
    def get_input(tic_tac_toe: TextTacToe) -> Coord:
        """
        Finds the best move using minimax algorithm
        """
        best_score = -float('inf')
        for coord in MinimaxBotInput.get_avaliable_coords(tic_tac_toe, tic_tac_toe.board):
            score = MinimaxBotInput.minimax_algorithm(tic_tac_toe, tic_tac_toe.board, coord, tic_tac_toe.current_turn, 10, True)
            if score > best_score:
                best_score = score
                best_coord = coord
        return best_coord

    @staticmethod
    def minimax_algorithm(tic_tac_toe: TextTacToe, board: [[Team]], new_coord: Coord, turn: Team, depth: int, maximizing: bool) -> int:
        """
        performs the minimax algorithm on a tic tac toe board
        """
        board[new_coord.y][new_coord.x] = turn
        avaliable_coords = MinimaxBotInput.get_avaliable_coords(tic_tac_toe, board)
        if depth == 0:
            return 0
        elif (winner := tic_tac_toe._detect_winner(board)) is not None:
            if winner == Team.Empty:
                return 0
            elif winner == tic_tac_toe.current_turn:
                return 1
            else:
                return -1
        if maximizing:
            for coord in avaliable_coords:
                pass
        else:
            for coord in avaliable_coords:
                pass

class TextTacToe:
    """
    Text-based Tic tac toe game
    """
    def __init__(self, player_x: InputType = UserInput, player_o: InputType = UserInput, board_size: Coord = Coord(3, 3)):
        self.player = player_x
        self.player_x = player_x
        self.player_o = player_o
        self.board_size = board_size # set the size of a tic tac toe board
        self.teams = [team for team in Team if team != Team.Empty]
        self.reset()

    @staticmethod
    def _swap_current_turn(turn: Team) -> Team:
        """
        Change current turn to the opposite player; if it is x change to o and visa versa
        """
        return Team.X if turn == Team.O else Team.O

    def swap_current_turn(self):
        """
        Change current turn to the opposite player; if it is x change to o and visa versa
        """
        self.current_turn = Team.X if self.current_turn == Team.O else Team.O

    def print(self):
        """
        Print the tic tac toe board and its contents
        """
        for i in range(self.board_size.y): # cycle through y coords
            for j in range(self.board_size.x): # cycle through x coords
                # print values and vertical lines in between
                print(self.board[i][j].value + (' |' if j < self.board_size.x - 1 else ''), end='')
            if i < self.board_size.y - 1: # if this isn't the last loop
                print('\n--+--+--') # print horizontal lines between values
        print('') # newline

    def play_game(self):
        """
        play a single game of tic tac toe
        """
        while (winner := self.detect_winner()) is None:
            self.print()
            self.player = self.player_x if self.current_turn == Team.X else self.player_o
            try:
                pos = self.player.get_input(self)
                if pos.x >= self.board_size.x or pos.x < 0 or pos.y >= self.board_size.y or pos.y < 0:
                    raise ValueError('Coordinate out of bounds')
                if self.board[pos.y][pos.x] != Team.Empty:
                    raise ValueError('Cannot place peice in spot that isnt empty')
            except ValueError as error:
                print(error)
                continue
            self.board[pos.y][pos.x] = self.current_turn
            self.swap_current_turn()
        self.print()
        if winner != Team.Empty:
            print(f'{winner.value} wins!')
        else:
            print('Cat\'s Game!')

    def detect_winner(self) -> Team:
        """
        detects if someone has won the game of tic tac toe.
        returns the team of the winner or None if there is no winner yet
        """
        return self._detect_winner(self.board)

    def _detect_winner(self, board: [[Team]]) -> Team:
        """
        detects if someone has won the game of tic tac toe.
        returns the team of the winner or None if there is no winner yet
        """
        check_diag = self.board_size.x == self.board_size.y
        for team in self.teams:
            horiz_win = [True for _ in range(self.board_size.x)]
            slope_down_diag_win = check_diag
            slope_up_diag_win = check_diag
            board_full = True
            for i in range(self.board_size.y): # cycle through y values
                if check_diag:
                    if board[i][i] != team:
                        slope_down_diag_win = False
                    if board[self.board_size.y - 1 - i][i] != team:
                        slope_up_diag_win = False
                for j in range(self.board_size.x):
                    if board[i][j] != team:
                        horiz_win[j] = False
                    if board[i][j] == Team.Empty:
                        board_full = False
                if board[i] == [team for _ in range(self.board_size.x)]:
                    return team
            if True in horiz_win or slope_up_diag_win or slope_down_diag_win:
                return team
        if board_full:
            return Team.Empty
        return None

    @staticmethod
    def get_matrix(x: int, y: int) -> [[Team]]:
        """
        Create new matric with width x and height y
        """
        return [[Team.Empty for j in range(x)] for i in range(y)]

    def reset(self):
        """
        Reset the board and the current turn
        """
        self.board = self.get_matrix(self.board_size.x, self.board_size.y) # create empty tic tac toe board
        self.current_turn = Team.X
        self.player = self.player_x if self.current_turn == Team.X else self.player_o
