import the_pink_coder.game.move
import the_pink_coder.board as board
from copy import deepcopy

class Player:
    
    def __init__(self, player):
        self.ally = player

        if ally == "upper":
            self.oppo = "lower"
        else:
            self.oppo = "lower"
        
        self.board = board.Board(ally, oppo)
        self.ally_throw_remain = 9
        self.oppo_throw_remain = 9
        ## 0 or 1 ???
        self.round = 1
        self.available_ally_throws = []
        self.available_oppo_throws = []
        self.type = ["r", "p", "s"]
        self.all_index = {4: (-4, 0), 3: (-4, 1), 2: (-4, 2), 1: (-4, 3), 0: (-4, 4), -1: (-3, 4), -2: (-2, 4), -3: (-1, 4), -4: (0, 4)}


    def action(self):
        
        self.update_available_throw()

        possible_ally_actions = self.get_actions("ally")

        possible_oppo_actions = self.get_actions("oppo")

        best_action = self.get_best_action(possible_ally_actions, possible_oppo_actions)

        # Round Increament
        self.round += 1
        
        return best_action

    
    def update(self, ally_action, oppo_action):

        if ally_action[0] == "THROW":
            self.ally_throw_remain -= 1
        if oppo_action[0] == "THROW":
            self.opponent_throw_remain -= 1
        
        self.board.update_board(ally_action, oppo_action)


    def generate_best_action(self, possible_ally_actions, possible_oppo_actions):
        for action in possible_ally_actions:
            for action_opp in possible_oppo_actions:
                board = deepcopy(self.board)
                board.update_board(action_opp, action)


    def update_available_throw(self):

        # Update ally throws
        id = getattr(self, "ally") 
        throw = getattr(self, "ally_throw_remain")
        available_throws = getattr(self, "available_ally_throws")

        for i in range (0, 2, 1):
            if throw > 0:
                if id == "upper":
                    line = 4 - (9 - throw)
                    min_Col = self.all_index[line][0]
                    max_Col = self.all_index[line][1]
                    if (line, min_Col) in available_throws:
                        pass
                    else:
                        for j in range(min_Col,max_Col+1):
                            available_throws.append((line, i))
                else:
                    line = -4 + (9 - throw)
                    min_Col = self.all_index[line][0]
                    max_Col = self.all_index[line][1]
                    if (line, min_Col) in available_throws:
                        pass
                    else:
                        for j in range(min_Col,max_Col+1):
                            available_throws.append((line, i))
            
            ## Update opponent throws
            id = getattr(self, "oppo") 
            throw = getattr(self, "oppo_throw_remain")
            available_throws = getattr(self, "available_oppo_throws")


    def get_actions(self, id):

        possible_throw_actions = []
        possible_move_actions = []

        if id == "ally":
            throw_remain = self.ally_throw_remain
        elif id == "oppo"
            throw_remain = self.oppo_throw_remain

        if throw_remain > 0:
            possible_throw_action = self.get_throws(id)
            
        all_token = self.board.board[getattr(self, id)]

        for i in all_token:
            action_list = game.move(i)
            for index in action_list:  
                possible_move_action.append((i[0], index, (i[1])))

    return possible_move_actions + possible_throw_actions


    def get_throws(self, id):
        
        possible_throws = []
        
        if id == "ally":
            available_throws = self.available_ally_throws
        elif id == "oppo":
            available_throws = self.available_oppo_throws
        
        for i in self.type:
            for j in available_throws:
                possible_throws.append(("THROW",i,j))
        
    return possible_throws


def main():
    player = Player("upper")
    player.action()
    print(player.round)
    print(player.possible_throw_position)
    player.update(("THROW","s",(4,1)),("THROW","p",(4,0)))
    player.update(("THROW","s",(4,1)),("THROW","p",(3,0)))
    print(player.board)
    player.action()


main()