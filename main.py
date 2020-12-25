"""This module is driver code for TextTacToe"""

from text_tac_toe import TextTacToe, RandomBotInput, MinimaxBotInput, Coord
from gui_tac_toe import GuiTacToe

if __name__ == '__main__':
    # gtt = GuiTacToe(player_o = MinimaxBotInput)
    gtt = GuiTacToe(player_o = RandomBotInput)
    gtt.play_game()
    # ttt = TextTacToe()
    # ttt.play_game()
