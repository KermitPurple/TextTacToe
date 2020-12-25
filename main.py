"""This module is driver code for TextTacToe"""

from text_tac_toe import TextTacToe, RandomBotInput

if __name__ == '__main__':
    ttt = TextTacToe()
    ttt.play_game(player_o = RandomBotInput)
