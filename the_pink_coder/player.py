import the_pink_coder.gametheory as gt
import the_pink_coder.game as game
import the_pink_coder.board as board
from copy import deepcopy
import random

class Player:
    
    def __init__(self, player):
        self.ally = player
        if self.ally == "upper":
            self.oppo = "lower"
        else:
            self.oppo = "upper"
        self.board = board.Board(self.ally, self.oppo)
        self.round = 0
        self.history_action = []
        self.board.update_available_throw()

    # Return an anction based on current board status
    def action(self):
        self.round += 1
        best_action = self.board.generate_best_action()
        return best_action

    # Update the current board of our player
    def update(self, oppo_action, ally_action):
        self.board.update_board(oppo_action, ally_action, True) 








    