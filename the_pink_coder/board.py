import math
import the_pink_coder.game as game
from copy import deepcopy
import the_pink_coder.gametheory as gt
import numpy as np

class Board:
    
    def __init__(self, ally, oppo, board={"upper": [], "lower": []}):
        self.ally = ally
        self.oppo = oppo
        self.board = board
        self.available_ally_throws = []
        self.available_oppo_throws = []
        self.possible_ally_throws = []
        self.ally_throw_remain = 9
        self.oppo_throw_remain = 9
        self.type = ["r", "p", "s"]
        self.all_index = {4: (-4, 0), 3: (-4, 1), 2: (-4, 2), 1: (-4, 3), 0: (-4, 4), -1: (-3, 4), -2: (-2, 4), -3: (-1, 4), -4: (0, 4)}
        self.last_position = ()


    def update_board(self, oppo_action, ally_action, printRes):
        
        if ally_action[0] == "THROW":
            self.ally_throw_remain -= 1
        if oppo_action[0] == "THROW":
            self.oppo_throw_remain -= 1



        # Update ally action
        id = getattr(self, "ally")
        action = ally_action

        self.last_position = ally_action
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
                if game.same_coord(i, j) and game.defeat(i, j):
                    self.board["upper"].remove(j)

            for k in self.board["lower"]:
                if game.same_coord(i, k) and game.defeat(i, k):
                    self.board["lower"].remove(k)



        self.update_available_throw()


    def distance(self, piece_1, piece_2):
        coord_1 = game.get_coord(piece_1)
        coord_2 = game.get_coord(piece_2)
        return math.sqrt(pow(coord_1[0] - coord_2[0], 2) + pow(coord_1[1] - coord_2[1], 2))


    
    


    # Generate evaluative value for one actions
    def evaluation(self, old_board):   
        
        score = 0

        distance_score = 0
        for i in self.board[self.ally]:
            min_defeated = 300
            max_defeated = -300
            count = 0
            for j in self.board[self.oppo]: 
                current_score = game.defeat_score(i[0], j[0], (12 - game.distance(i, j)))
                if current_score < 0 and current_score > max_defeated:
                    max_defeated = current_score
                elif current_score > 0 and current_score < min_defeated:
                    min_defeated = current_score
            if min_defeated == 300:
                min_defeated = 0
            if max_defeated == -300:
                max_defeated = 0
            distance_score += min_defeated+max_defeated

    
                # score += game.defeat_score(i[0], j[0], (12 - self.distance(i, j)))

        diff_ally = len(old_board.board[self.ally]) - len(self.board[self.ally])
        diff_oppo = len(old_board.board[self.oppo]) - len(self.board[self.oppo])
        # score += distance_score

        # if len(self.board[self.ally]) < len(old_board.board[self.ally]):
        #     score -= (len(old_board.board[self.ally]) - len(self.board[self.ally])) * 12
        # if len(self.board[self.oppo]) < len(old_board.board[self.oppo]):
        #     score += (len(old_board.board[self.oppo]) - len(self.board[self.oppo])) * 12

        # if len(self.board[self.oppo]) == len(old_board.board[self.oppo]):
        #         score -= 2
        if len(self.board[self.ally]) != 0:

            distance_score =  distance_score / len(self.board[self.ally])

        if diff_ally < 0:
            diff_ally = 0
        if diff_oppo < 0:
            diff_oppo = 0

        score = 1*distance_score - 12 * diff_ally + 12 * diff_oppo


        # if score > 0:
        #     if len(self.board[self.ally]) == 0 and len(self.board[self.oppo]) == 0:
        #         score = score
        #     elif len(self.board[self.oppo]) == 0:
        #         score = score / (len(self.board[self.ally]))
        #     elif len(self.board[self.ally]) == 0:
        #         score = score / (len(self.board[self.oppo]))
        #     else:
        #         score = score / (len(self.board[self.ally])+len(self.board[self.oppo]))
            
        return score

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
                        available_throws.clear()
                        for j in range(min_Col,max_Col+1):
                            available_throws.append((line, j))
                            if i == 0:
                                self.possible_ally_throws.append((line, j))
                else:
                    line = -4 + (9 - throw)
                    min_Col = self.all_index[line][0]
                    max_Col = self.all_index[line][1]
                    if (line, min_Col) in available_throws:
                        pass
                    else:
                        available_throws.clear()
                        for j in range(min_Col,max_Col+1):
                            available_throws.append((line, j))
                            if i == 0:
                                self.possible_ally_throws.append((line, j))
            
            ## Update opponent throws
            id = getattr(self, "oppo") 
            throw = getattr(self, "oppo_throw_remain")
            available_throws = getattr(self, "available_oppo_throws")


    def generate_best_action(self):

        dict = {"r":0,"p":0,"s":0}
        for peice in self.board[self.ally]:
            dict[peice[0]] += 1
        
        size_ally = len(self.board[self.ally])


        oppo_type = []
        for oppo in self.board[self.oppo]:
            if oppo[0] not in oppo_type:
                oppo_type.append(oppo[0])



        # Kill directly
        possible_ally_actions = []
        if self.ally_throw_remain > 2:
            for piece in self.board[self.oppo]:
                if piece[1] in self.possible_ally_throws:
                    if (piece[0] == 'r' and dict["p"]/size_ally < 0.35) or (piece[0] == 'r' and self.oppo_throw_remain == 0):
                        possible_ally_actions.append(("THROW", "p", (piece[1])))
                    elif (piece[0] == 'p' and dict["s"]/size_ally < 0.35) or (piece[0] == 'p' and self.oppo_throw_remain == 0):
                        possible_ally_actions.append(("THROW", "s", (piece[1])))
                    elif (piece[0] == 's' and dict["r"]/size_ally < 0.35) or (piece[0] == 's' and self.oppo_throw_remain == 0):
                        possible_ally_actions.append(("THROW", "r", (piece[1])))

        if len(possible_ally_actions) > 0:

            percentage = 1 - (1 / len(self.board[self.oppo]))


            if percentage >= 0.5:
                possible_ally_actions = possible_ally_actions 
            elif len(self.board[self.oppo]) == 1 or len(oppo_type) == 1:
                possible_ally_actions = possible_ally_actions
            # if self.ally_throw_remain > 5 and percentage > 0.4:
            #     possible_ally_actions = possible_ally_actions
            # elif self.ally_throw_remain > 3 and percentage > 0.6:
            #     possible_ally_actions = possible_ally_actions
            # elif percentage > 0.8:
            #     possible_ally_actions = possible_ally_actions
            else:
                possible_ally_actions = []


    
        if len(possible_ally_actions) == 1:
                return possible_ally_actions[0] 

        if len(possible_ally_actions) == 0:
            possible_ally_actions = self.get_actions("ally")

        possible_oppo_actions = self.get_actions("oppo")

        # print(self.board)
        # print(possible_ally_actions)
        # print(possible_oppo_actions)


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
                board = deepcopy(self)
                board.update_board(oppo_action, ally_action, False)
                temp_array.append(board.evaluation(self))
            
            matrix.append(temp_array)

        list_res , expect = gt.solve_game(matrix)

        possible_ally_actions_2 = []


        max_score = max(list_res)
        best_action = possible_ally_actions[list(list_res).index(max_score)]



        

        possible_ally_actions_2.append(best_action)
        np.delete(list_res, list(list_res).index(max_score))

        max_score = max(list_res)
        best_action = possible_ally_actions[list(list_res).index(max_score)]
        possible_ally_actions_2.append(best_action)

        # print(possible_ally_actions_2)
        matrix = []
        for ally_action in possible_ally_actions_2:
                
            temp_array = []
            
            for oppo_action in possible_oppo_actions:
                board = deepcopy(self)
                board.update_board(oppo_action, ally_action, False)
                temp_array.append(board.multi_stage())
            
            matrix.append(temp_array)

        list_res2 , expect = gt.solve_game(matrix)

        max_score = max(list_res2)
        best_action_res = possible_ally_actions_2[list(list_res2).index(max_score)]


        return best_action_res



    # def multi_stage_depth_2(self, matrix):
    #     lsit_res, expected = gt.solve_game(matrix)



    def get_actions(self, id):
    
        possible_throw_actions = []
        possible_move_actions = []

        if id == "ally":
            throw_remain = self.ally_throw_remain
            oppo_id = "oppo"
        elif id == "oppo":
            throw_remain = self.oppo_throw_remain
            oppo_id = "ally"

        if throw_remain > 0:
            possible_throw_actions = self.get_throws(id)

            
        all_token = self.board[getattr(self, id)]

        oppo_type = []
        for oppo in self.board[getattr(self, oppo_id)]:
            oppo_type.append(oppo[0])

        dict = {"r": 9999, "p":9999,"s":9999}

        dict_piece = {}


        defeated_distance = 9999


        moveable = []
        
        for i in all_token:
            flag = 0
            for oppo in self.board[getattr(self, oppo_id)]:
                if game.defeat(i, oppo) and game.distance(i, oppo) < dict[i[0]]:
                    dict[i[0]] = game.distance(i, oppo)
                    dict_piece[i[0]] = i
                
                if flag == 0 and game.defeat(oppo, i) and game.distance(i, oppo) < 2:
                    flag = 1
                    moveable.append(i)
                

        for i in dict_piece:
            moveable.append(dict_piece[i])



        
        # 加一个离敌人最近的token？
        # if type != "":
        #     moveable.append(dict_piece[type])
        if len(moveable) == 0:
            moveable = all_token

        for i in moveable:
            if len(oppo_type) == 1 and i[0] in oppo_type:
                continue
            action_list = game.move(self, i, id)
            slide_move = game.slide(i)
            for index in action_list:
                if index in slide_move and ("SLIDE", index, i[1]) != self.last_position: 
                    possible_move_actions.append(("SLIDE", (i[1]), index))
                elif index not in slide_move and ("SWING", index, i[1]) != self.last_position:
                    possible_move_actions.append(("SWING", (i[1]), index))
                else:
                    pass
        

        

        current_index = []
        for piece in self.board[self.ally]:
            current_index.append(piece[1])

        for action in possible_move_actions:
            if action[2] in current_index:
                # print(action[2])
                # print(current_index)
                possible_move_actions.remove(action)
        
        for action in possible_throw_actions:
            if action[2] in current_index:
                # print(action[2])
                # print(current_index)
                possible_throw_actions.remove(action)

        # print(possible_throw_actions)
        # print(possible_move_actions)
        # if len(possible_throw_actions) > 0:
        #     return possible_throw_actions

        return possible_move_actions + possible_throw_actions




    def get_throws(self, id):
        possible_throws = []
        
        if id == "ally":
            available_throws = self.available_ally_throws
        elif id == "oppo":
            available_throws = self.available_oppo_throws


        wanted_type = ["r","p","s"]
        if id == "ally":
            current_type_ally = []
            for piece in self.board[self.ally]:
                if piece[0] not in current_type_ally:
                    current_type_ally.append(piece[0])
            

            current_type_oppo = []
            for piece in self.board[self.oppo]:
                if piece[0] not in current_type_oppo:
                    current_type_oppo.append(piece[0])

            if ('r' in current_type_oppo and 'p' in current_type_ally) or 'r' not in current_type_oppo:
                wanted_type.remove('p')
            if ('s' in current_type_oppo and 'r' in current_type_ally) or 's' not in current_type_oppo:
                wanted_type.remove('r')
            if ('p' in current_type_oppo and 's' in current_type_ally) or 'p' not in current_type_oppo:
                wanted_type.remove('s')

 
            if len(wanted_type) == 0 and self.oppo_throw_remain == 9:
                wanted_type = self.type
        
        if id == "oppo":
            current_type_ally = []
            for piece in self.board[self.oppo]:
                if piece[0] not in current_type_ally:
                    current_type_ally.append(piece[0])
            

            current_type_oppo = []
            for piece in self.board[self.ally]:
                if piece[0] not in current_type_oppo:
                    current_type_oppo.append(piece[0])

            if ('r' in current_type_oppo and 'p' in current_type_ally) or 'r' not in current_type_oppo:
                wanted_type.remove('p')
            if ('s' in current_type_oppo and 'r' in current_type_ally) or 's' not in current_type_oppo:
                wanted_type.remove('r')
            if ('p' in current_type_oppo and 's' in current_type_ally) or 'p' not in current_type_oppo:
                wanted_type.remove('s')


            if len(wanted_type) == 0 and self.ally_throw_remain == 9:
                wanted_type = self.type
        

        for i in wanted_type:
            for j in available_throws:
                possible_throws.append(("THROW",i,j))
        
        return possible_throws




    def multi_stage(self):
        
        possible_ally_actions = self.get_actions("ally")
        possible_oppo_actions = self.get_actions("oppo")

        matrix = []
        better_action = []
        for ally_action in possible_ally_actions:
            temp_array = []
            for oppo_action in possible_oppo_actions:
                board = deepcopy(self)
                board.update_board(oppo_action, ally_action, False)
                temp_array.append(board.evaluation(self))
            matrix.append(temp_array)
        
        list_res , expect = gt.solve_game(matrix)

        return expect