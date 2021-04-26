import math
import the_pink_coder.game as game

class Board:
    
    def __init__(self, ally, oppo, board={"upper": [], "lower": []}):
        self.ally = ally
        self.oppo = oppo
        self.board = board


    def update_board(self, oppo_action, ally_action):
        
        # Update ally action
        id = getattr(self, "ally")
        action = ally_action
              
        for i in range(0, 2, 1):       
            if action[0] == "THROW":
                self.board[id].append([action[1],(action[2][0],action[2][1])])
            else:
                for piece in self.board[id]:
                    index = piece[1]
                    if index == action[1]:
                        new_piece = [piece[0],(action[2][0], action[2][1])]
                        self.board[id].remove(piece)
                        self.board[id].append(new_piece)
                        break
                        
            
            # Update opponent action
            id = getattr(self, "oppo")
            action = oppo_action


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
    def evaluation(self):   
        
        score = 0
        # score += len(self.board[self.ally])
        # score -= len(self.board[self.oppo])

        for i in self.board[self.ally]:
            for j in self.board[self.oppo]: 
                score += game.defeat_score(i[0], j[0], (9 - self.distance(i, j)))
        # print(self.board)
        if len(self.board[self.oppo]) == 0:
            score = score / (len(self.board[self.ally]))
        elif len(self.board[self.ally]) == 0:
            score = score / (len(self.board[self.oppo]))
        else:
            score = score / (len(self.board[self.ally])*len(self.board[self.oppo]))
        return score


def get_closest_defeated_index(self, upper_index, board):
        distance = float('inf');
        cloest_index = None;
        for j in board[self.game.enemy]:
            if self.game.defeated(upper_index, j) is 'win' and dist(upper_index,j)<distance:
                cloest_index = j
        return cloest_index

