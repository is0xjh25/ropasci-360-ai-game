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
        self.ally_throw_remain = 9
        self.oppo_throw_remain = 9
        self.round = 0
        self.available_ally_throws = []
        self.available_oppo_throws = []
        self.type = ["r", "p", "s"]
        self.all_index = {4: (-4, 0), 3: (-4, 1), 2: (-4, 2), 1: (-4, 3), 0: (-4, 4), -1: (-3, 4), -2: (-2, 4), -3: (-1, 4), -4: (0, 4)}

        self.history_action = []


    def action(self):

        self.board.update_available_throw()
        possible_ally_actions = self.board.get_actions("ally")

        possible_oppo_actions = self.board.get_actions("oppo")
        # print(possible_ally_actions)
        # print(possible_oppo_actions)
        # Round Increament
        self.round += 1

        best_action = self.generate_best_action(possible_ally_actions, possible_oppo_actions)
        return best_action

    
    def update(self, oppo_action, ally_action):

        if ally_action[0] == "THROW":
            self.ally_throw_remain -= 1
        if oppo_action[0] == "THROW":
            self.oppo_throw_remain -= 1
        
        self.board.update_board(oppo_action, ally_action, True)


    def generate_best_action(self, possible_ally_actions, possible_oppo_actions):
        
        matrix = []
        better_action = []

        # for ally_action in possible_ally_actions:
        #     killer = 0
        #     for oppo_action in possible_oppo_actions:
        #         board = deepcopy(self.board)
        #         board.update_board(oppo_action, ally_action, False)
        #         if len(board.board[self.oppo]) < len(self.board.board[self.oppo]) and len(board.board[self.ally]) == len(self.board.board[self.ally]):
        #             # return ally_action
        #             killer = 1
        #             break
        #     if killer == 1:
        #         better_action.append(ally_action)

        # if len(better_action) > 0:
        #     possible_ally_actions = better_action
        # TODO: 30/4

        # 1. action的某一个eval过低，直接抛弃这个action
        # 2. 减少不必要的出棋子：generation action
                # -  缺什么才出什么，而不是直接出3种棋子 (Finished)



        # 3. 重合的棋子 有了所有action判断 (Finished)
        # 1. action的某一个eval过低，直接抛弃这个action
        # 4. 吃自己的棋子 



        # 4. Balance 的问题



        for ally_action in possible_ally_actions:
            
            temp_array = []
            
            for oppo_action in possible_oppo_actions:
                board = deepcopy(self.board)
                board.update_board(oppo_action, ally_action, False)
                
                # 一个function 解决： 返回Expected Value( 和 Matrix)
                # board.futhre_board(times, throw, throw) 
                # 
                # Function in board 
                # temp_array.append(board.futhre_board());
                temp_array.append(board.evaluation(self.board))
            
            matrix.append(temp_array)

        # matrix [possible action] [oppo action]


        # print(possible_ally_actions)
        # print(possible_oppo_actions)
        # print(matrix)


        list_res , expect = gt.solve_game(matrix)
        max_score = max(list_res)



        best_action = possible_ally_actions[list(list_res).index(max_score)]

        return best_action
        
    


    # def update_available_throw(self):

    #     # Update ally throws
    #     id = getattr(self, "ally") 
    #     throw = getattr(self, "ally_throw_remain")
    #     available_throws = getattr(self, "available_ally_throws")

    #     for i in range (0, 2, 1):
    #         if throw > 0:
    #             if id == "upper":
    #                 line = 4 - (9 - throw)
    #                 min_Col = self.all_index[line][0]
    #                 max_Col = self.all_index[line][1]
    #                 if (line, min_Col) in available_throws:
    #                     pass
    #                 else:
    #                     for j in range(min_Col,max_Col+1):
    #                         available_throws.append((line, j))
    #             else:
    #                 line = -4 + (9 - throw)
    #                 min_Col = self.all_index[line][0]
    #                 max_Col = self.all_index[line][1]
    #                 if (line, min_Col) in available_throws:
    #                     pass
    #                 else:
    #                     for j in range(min_Col,max_Col+1):
    #                         available_throws.append((line, j))
            
    #         ## Update opponent throws
    #         id = getattr(self, "oppo") 
    #         throw = getattr(self, "oppo_throw_remain")
    #         available_throws = getattr(self, "available_oppo_throws")


    # def get_actions(self, id):

    #     possible_throw_actions = []
    #     possible_move_actions = []

    #     if id == "ally":
    #         throw_remain = self.ally_throw_remain
    #     elif id == "oppo":
    #         throw_remain = self.oppo_throw_remain

    #     if throw_remain > 0:
    #         possible_throw_actions = self.get_throws(id)

            
    #     all_token = self.board.board[getattr(self, id)]

    #     for i in all_token:
    #         action_list = game.move(self.board, i, id)
    #         slide_move = game.slide(i)
    #         for index in action_list: 
    #             if index in slide_move: 
    #                 possible_move_actions.append(("SLIDE", (i[1]), index))
    #             else:
    #                 possible_move_actions.append(("SWING", (i[1]), index))

    #     current_index = []
    #     for piece in self.board.board[self.ally]:
    #         current_index.append(piece[1])

    #     for action in possible_move_actions:
    #         if action[2] in current_index:
    #             possible_move_actions.remove(action)
        
    #     for action in possible_throw_actions:
    #         if action[2] in current_index:
    #             possible_throw_actions.remove(action)



        
    #     return possible_move_actions + possible_throw_actions


    # def get_throws(self, id):
        
    #     possible_throws = []
        
    #     if id == "ally":
    #         available_throws = self.available_ally_throws
    #     elif id == "oppo":
    #         available_throws = self.available_oppo_throws


    #     wanted_type = ["r","p","s"]
    #     if id == "ally":
    #         current_type_ally = []
    #         for piece in self.board.board[self.ally]:
    #             if piece[0] not in current_type_ally:
    #                 current_type_ally.append(piece[0])
            

    #         current_type_oppo = []
    #         for piece in self.board.board[self.oppo]:
    #             if piece[0] not in current_type_oppo:
    #                 current_type_oppo.append(piece[0])
    #         # print(current_type_ally)
    #         # print(current_type_oppo)
    #         if ('r' in current_type_oppo and 'p' in current_type_ally) or 'r' not in current_type_oppo:
    #             wanted_type.remove('p')
    #         if ('s' in current_type_oppo and 'r' in current_type_ally) or 's' not in current_type_oppo:
    #             wanted_type.remove('r')
    #         if ('p' in current_type_oppo and 's' in current_type_ally) or 'p' not in current_type_oppo:
    #             wanted_type.remove('s')

 
    #         if len(wanted_type) == 0 and len(current_type_oppo)== 0:
    #             wanted_type = self.type
            

    #     # print(wanted_type, id)

    #     for i in wanted_type:
    #         for j in available_throws:
    #             possible_throws.append(("THROW",i,j))
        
    #     return possible_throws






