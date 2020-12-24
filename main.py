from __future__ import annotations # allows for use of Coord in function type declarations

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
        s = (''.join(map(lambda ch: ch if ch.isnumeric() else ' ', string))).split(' ') # split input string into list of empy strings and numbers
        while '' in s: # While there are empty strings
            s.remove('') # remove an empty string
        length = len(s)
        if length < 2:
            raise ValueError("Not enough numbers for a coordinate in a 2d plane")
        elif length > 2:
            raise ValueError("Too many numbers for a coordinate in a 2d plane")
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

    def print(self):
        """
        Print the tic tac toe board and its contents
        """
        for i in range(self.size.y): # cycle through y coords
            for j in range(self.size.x): # cycle through x coords
                print(self.board[i][j] + (' |' if j < self.size.x - 1 else ''), end='') # print values and vertical lines in between
            if i < self.size.y - 1: # if this isn't the last loop
                print('\n--+--+--') # print horizontal lines between values
        print('') # newline

    @staticmethod
    def get_user_input() -> Coord:
        """
        get user input and covert it to a Coord
        """
        return Coord.from_string(input('Enter a valid Coordinate on the board: '))

    @staticmethod
    def get_matrix(x: int, y: int) -> [[int]]:
        """
        Create new matric with width x and height y
        """
        return [[' ' for j in range(x)] for i in range(y)]

if __name__ == '__main__':
    ttt = TextTacToe()
    ttt.print()
    print(ttt.get_user_input())
