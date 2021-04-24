class Board:
    def __init__(self):
        self.current_board = {"upper": [], "lower": []}

    def update_board(self, opponent_action, player_action):

        if opponent_action[0] == "THROW":
            self.current_board[self.opponent].append([opponent_action[1],(opponent_action[2][0],opponent_action[2][1])])
        else:
            for piece in self.current_board[self.opponent]:
                index = piece[1]
                if index == opponent_action[2]:
                    new_piece = [piece[0],(opponent_action[1][0],opponent_action[1][0])]
                    self.current_board[self.opponent].remove(piece)
                    self.current_board[self.opponent].append(new_piece)


        if player_action[0] == "THROW":
            self.current_board[self.player].append([player_action[1],(player_action[2][0],player_action[2][1])])
        else:
            for piece in self.current_board[self.player]:
                index = piece[1]
                if index == player_action[2]:
                    new_piece = [piece[0],(player_action[1][0],player_action[1][0])]
                    self.current_board[self.player].remove(piece)
                    self.current_board[self.player].append(new_piece)




    def evaluation_value(self):
