import the_pink_coder.game.defeat

class Board:
    
    def __init__(self, ally, oppo, board={"upper": [], "lower": []}):
        self.ally = ally
        self.oppo = oppo
        self.board = board


    def update_board(self, ally_action, oppo_action):
        
        # Update ally action
        id = getattr(self, "ally")
        action = ally_action
              
        for i in range(0, 2, 1):       
            if action[0] == "THROW":
                self.board[id].append([action[1],(action[2][0],action[2][1])])
            else:
                for piece in self.board[identity]:
                    index = piece[1]
                    if index == action[2]:
                        new_piece = [piece[0],(action[1][0], action[1][1])]
                        self.board[identity].remove(piece)
                        self.board[identity].append(new_piece)
            
            # Update opponent action
            id = getattr(self, "oppo")
            action = oppo_action
        
        # Update combat result
        tokens = self.board["upper"] + self.board["lower"]
        
        for i in tokens:

            for j in self.board["upper"]:
                if defeat(i, j):
                    self.board["upper"].remove(j)

            for k in self.board["lower"]:
                if defeat(i, k):
                    self.board["lower"].remove(k)


    # Generate evaluative value for one actions
    def evaluation(self):   
        score = 0

