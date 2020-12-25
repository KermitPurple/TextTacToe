"""Contains three classes used for a text-based TicTacToe game"""

from __future__ import annotations # allows for use of Coord in function type declarations
from enum import Enum

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

    @staticmethod
    def from_string(string: str) -> Coord:
        """
        Create a new Coord object from a string
        """
        # split input string into list of empy strings and numbers
        s = (''.join(map(lambda ch: ch if ch.isnumeric() else ' ', string))).split(' ')
        while '' in s: # While there are empty strings
            s.remove('') # remove an empty string
        length = len(s)
        if length < 2:
            raise ValueError('Not enough numbers for a coordinate in a 2d plane')
        if length > 2:
            raise ValueError('Too many numbers for a coordinate in a 2d plane')
        return Coord(int(s[0]), int(s[1]))

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

class TextTacToe:
    """
    Text-based Tic tac toe game
    """
    def __init__(self):
        self.size = Coord(3, 3) # set the size of a tic tac toe board
        self.board = self.get_matrix(self.size.x, self.size.y) # create empty tic tac toe board
        self.current_turn = Team.X
        self.teams = [team for team in Team if team != Team.Empty]

    def swap_current_turn(self):
        """
        Change current turn to the opposite player; if it is x change to o and visa versa
        """
        self.current_turn = Team.X if self.current_turn == Team.O else Team.O

    def print(self):
        """
        Print the tic tac toe board and its contents
        """
        for i in range(self.size.y): # cycle through y coords
            for j in range(self.size.x): # cycle through x coords
                # print values and vertical lines in between
                print(self.board[i][j].value + (' |' if j < self.size.x - 1 else ''), end='')
            if i < self.size.y - 1: # if this isn't the last loop
                print('\n--+--+--') # print horizontal lines between values
        print('') # newline

    def play_game(self):
        """
        play a single game of tic tac toe
        """
        while (winner := self.detect_winner()) is None:
            self.print()
            try:
                pos = self.get_user_input()
                if pos.x >= self.size.x or pos.x < 0 or pos.y >= self.size.y or pos.y < 0:
                    raise ValueError('Coordinate out of bounds')
                if self.board[pos.y][pos.x] != Team.Empty:
                    raise ValueError('Cannot place peice in spot that isnt empty')
            except ValueError as e:
                print(e)
                continue
            self.board[pos.y][pos.x] = self.current_turn
            self.swap_current_turn()
        print(f'{winner.value} wins!')

    def detect_winner(self) -> Team:
        """
        detects if someone has won the game of tic tac toe.
        returns the team of the winner or None if there is no winner yet
        """
        check_diag = self.size.x == self.size.y
        for team in self.teams:
            horiz_win = [True for _ in range(self.size.x)]
            diag_win = True
            for i in range(self.size.y): # cycle through y values
                if check_diag:
                    if self.board[i][i] != team:
                        diag_win = False
                for j in range(self.size.x):
                    if self.board[i][j] != team:
                        horiz_win[j] = False
                if self.board[i] == [team for _ in range(self.size.x)]:
                    return team
            if True in horiz_win or diag_win:
                return team
        return None

    @staticmethod
    def get_user_input() -> Coord:
        """
        get user input and covert it to a Coord
        """
        return Coord.from_string(input('Enter a valid Coordinate on the board: '))

    @staticmethod
    def get_matrix(x: int, y: int) -> [[Team]]:
        """
        Create new matric with width x and height y
        """
        return [[Team.Empty for j in range(x)] for i in range(y)]
