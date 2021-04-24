import team_name.board as board
from copy import deepcopy

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class Player:
    
    def __init__(self, player):
        self.player = player

        if player == "upper":
            self.opponent = "lower"
        else:
            self.opponent = "lower"
        
        self.board = board.Board()
        self.remain_throw = 9
        self.opponent_throw = 9
        self.round = 0
        self.possible_throw_position = []
        self.possible_throw_position_opp = []
        self.type = ["r","p","s"]
        self.all_index = {4: (-4, 0), 3: (-4, 1), 2: (-4, 2), 1: (-4, 3), 0: (-4, 4), -1: (-3, 4), -2: (-2, 4), -3: (-1, 4), -4: (0, 4)}
        """
        Called once at the beginning of a game to initialise this player.
        Set up an internal representation of the game state.

        The parameter player is the string "upper" (if the instance will
        play as Upper), or the string "lower" (if the instance will play
        as Lower).
        """
        # put your code here

    def action(self):
        self.update_possible_throw()

        possible_action = self.get_all_action()

        possible_action_opp = self.get_all_action_opp()
        
        best_action = self.generate_best_action(possible_action, possible_action_opp) 

        """
        Called at the beginning of each turn. Based on the current state
        of the game, select an action to play this turn.
        """
        # put your code here
    
    def update(self, opponent_action, player_action):
        """
        Called at the end of each turn to inform this player of both
        players' chosen actions. Update your internal representation
        of the game state.
        The parameter opponent_action is the opponent's chosen action,
        and player_action is this instance's latest chosen action.
        """
        if player_action[0] == "THROW":
            self.remain_throw -= 1
        if opponent_action[0] == "THROW":
            self.opponent_throw -= 1
        self.board.update_board(opponent_action, player_action)
        # put your code here


    def generate_best_action(slef, possible_action, possible_action_opp):
        for action in possible_action:
            for action_opp in possible_action_opp:
                board = deepcopy(self.board)
                board.update_board(action_opp, action)



    def update_possible_throw(self):
        if self.remain_throw > 0:
            if self.player == "upper":
                line = 4 - (9-self.remain_throw)
                min_Col = self.all_index[line][0]
                max_Col = self.all_index[line][1]
                if (line, min_Col) in self.possible_throw_position:
                    pass
                else:
                    for i in range(min_Col,max_Col+1):
                        self.possible_throw_position.append((line, i))
            else:
                line = -4 + (9-self.remain_throw)
                min_Col = self.all_index[line][0]
                max_Col = self.all_index[line][1]
                if (line, min_Col) in self.possible_throw_position_opp:
                    pass
                else:
                    for i in range(min_Col,max_Col+1):
                        self.possible_throw_position.append((line, i))
        if self.opponent_throw > 0:
            if self.player == "upper":
                line = -4 + (9-self.opponent_throw)
                min_Col = self.all_index[line][0]
                max_Col = self.all_index[line][1]
                if (line, min_Col) in self.possible_throw_position_opp:
                    pass
                else:
                    for i in range(min_Col,max_Col+1):
                        self.possible_throw_position_opp.append((line, i))
            else:
                line = 4 - (9-self.opponent_throw)
                min_Col = self.all_index[line][0]
                max_Col = self.all_index[line][1]
                if (line, min_Col) in self.possible_throw_position_opp:
                    pass
                else:
                    for i in range(min_Col,max_Col+1):
                        self.possible_throw_position_opp.append((line, i))





        
    def move(self, i):
        action_set = set(self.slide(i) + self.swing(i))
        action_list = list(action_set)

        return action_list




    def swing(self, index):
        possible_trans_index = self.slide(index)
        trans_index = []
        result_pieces = []
        for i in self.board.current_board[self.player]:
            if (i) in possible_trans_index:
                trans_index.append(i)

        for i in trans_index:
            result_pieces.append(self.slide(i))
        
        return result_pieces


    def slide(self, index):
        row = index[1][0]
        col = index[1][1]

        original_index = (row, col)
        possible_result_coord = [(row + 1, col - 1), (row + 1, col), (row, col - 1), (row, col + 1), (row - 1, col), (row - 1, col + 1)]

        result_pieces = []

        for i in possible_result_coord:
            if not self.out_boundary(i):
                result_pieces.append(i)

        return result_pieces


    
    def out_boundary(self, coord):
       
        row = coord[0]
        col = coord[1]

        dict_valid = {4: (-4, 0), 3: (-4, 1), 2: (-4, 2), 1: (-4, 3), 0: (-4, 4), -1: (-3, 4), -2: (-2, 4), -3: (-1, 4), -4: (0, 4)}
        
        if (row not in dict_valid.keys()):
            return True

        min_col = dict_valid[coord[0]][0]
        max_col = dict_valid[coord[0]][1]
               
        if col < min_col or col > max_col:
            return True
        
        return False

    def get_all_action(self):

        possible_throw_action = []
        possible_move_action = []

        if self.remain_throw > 0:
            possible_throw_action = self.get_all_throw()
        
        
        all_token = self.board.current_board[self.player]
        for i in all_token:
            action_list = self.move(i)
            for index in action_list:
                
                possible_move_action.append((i[0], index, (i[1])))
        return possible_move_action+possible_throw_action


    def get_all_action_opp(self):
    
        possible_throw_action = []
        possible_move_action = []

        if self.remain_throw > 0:
            possible_throw_action = self.get_all_throw_opp()
        
        
        all_token = self.board.current_board[self.opponent]
        for i in all_token:
            action_list = self.move(i)
            for index in action_list:
                
                possible_move_action.append((i[0], index, (i[1])))
        return possible_move_action+possible_throw_action
    

    def get_all_throw_opp(self):
        possible_throw_action = []
        for i in self.type:
            for j in self.possible_throw_position_opp:
                possible_throw_action.append(("THROW",i,j))
        return possible_throw_action




    def get_all_throw(self):
        possible_throw_action = []
        for i in self.type:
            for j in self.possible_throw_position:
                possible_throw_action.append(("THROW",i,j))
        return possible_throw_action



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