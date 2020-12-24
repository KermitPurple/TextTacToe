class TextTacToe:
    """
    Text-based Tic tac toe game
    """
    def __init__(self):
        pass

    @staticmethod
    def get_matrix(x: int, y: int) -> [[int]]:
        """
        Create new matric with width x and height y
        """
        return [[' ' for j in range(x)] for i in range(y)]

if __name__ == '__main__':
    for lst in TextTacToe.get_matrix(5, 3):
        print(lst)
