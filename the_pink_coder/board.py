import math
import the_pink_coder.game as game

class Board:
    
    def __init__(self, ally, oppo, board={"upper": [], "lower": []}):
        self.ally = ally
        self.oppo = oppo
        self.board = board


    def update_board(self, oppo_action, ally_action, printRes):
        
        # Update ally action
        id = getattr(self, "ally")
        action = ally_action


        if action[0] == "THROW":
            self.board[self.ally].append([action[1],(action[2][0],action[2][1])])
        else:
            for piece in self.board[self.ally]:
                index = piece[1]
                if index == action[1]:
                    new_piece = [piece[0],(action[2][0], action[2][1])]
                    self.board[self.ally].remove(piece)
                    self.board[self.ally].append(new_piece)
                    break
        
        action = oppo_action

        if action[0] == "THROW":
            self.board[self.oppo].append([action[1],(action[2][0],action[2][1])])
        else:
            for piece in self.board[self.oppo]:
                index = piece[1]
                if index == action[1]:
                    new_piece = [piece[0],(action[2][0], action[2][1])]
                    self.board[self.oppo].remove(piece)
                    self.board[self.oppo].append(new_piece)
                    break
        
        # Update combat result
        tokens = self.board["upper"] + self.board["lower"]
        
        for i in tokens:
            for j in self.board["upper"]:
                if game.defeat(i, j):
                    self.board["upper"].remove(j)

            for k in self.board["lower"]:
                if game.defeat(i, k):
                    self.board["lower"].remove(k)


    def distance(self, piece_1, piece_2):
        coord_1 = game.get_coord(piece_1)
        coord_2 = game.get_coord(piece_2)
        return math.sqrt(pow(coord_1[0] - coord_2[0], 2) + pow(coord_1[1] - coord_2[1], 2))


    
    


    # Generate evaluative value for one actions
    def evaluation(self, old_board):   
        
        score = 0

        for i in self.board[self.ally]:
            for j in self.board[self.oppo]: 
                score += game.defeat_score(i[0], j[0], (12 - self.distance(i, j)))
        if len(self.board[self.ally]) < len(old_board.board[self.ally]):
            score -= (len(old_board.board[self.ally]) - len(self.board[self.ally])) * 3
        if len(self.board[self.oppo]) < len(old_board.board[self.oppo]):
            score += (len(old_board.board[self.oppo]) - len(self.board[self.oppo])) * 3

        if len(self.board[self.oppo]) == len(old_board.board[self.oppo]):
                score -= 2
        if score > 0:
            if len(self.board[self.ally]) == 0 and len(self.board[self.oppo]) == 0:
                score = score
            elif len(self.board[self.oppo]) == 0:
                score = score / (len(self.board[self.ally]))
            elif len(self.board[self.ally]) == 0:
                score = score / (len(self.board[self.oppo]))
            else:
                score = score / (len(self.board[self.ally])+len(self.board[self.oppo]))
            
        return score


