class Coord:
    """
    a representation of an x and y coordinate
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
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

    @staticmethod
    def get_matrix(x: int, y: int) -> [[int]]:
        """
        Create new matric with width x and height y
        """
        return [[' ' for j in range(x)] for i in range(y)]

if __name__ == '__main__':
    ttt = TextTacToe()
    ttt.print()
