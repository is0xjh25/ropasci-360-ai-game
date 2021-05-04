import math
import the_pink_coder.game as game
from copy import deepcopy
import the_pink_coder.gametheory as gt

class Board:
    
    def __init__(self, ally, oppo, board={"upper": [], "lower": []}):
        self.ally = ally
        self.oppo = oppo
        self.board = board
        self.available_ally_throws = []
        self.available_oppo_throws = []
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
            score += (len(old_board.board[self.oppo]) - len(self.board[self.oppo])) * 8

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
                        if i == 1:
                            available_throws.clear()
                        for j in range(min_Col,max_Col+1):
                            
                            available_throws.append((line, j))
                else:
                    line = -4 + (9 - throw)
                    min_Col = self.all_index[line][0]
                    max_Col = self.all_index[line][1]
                    if (line, min_Col) in available_throws:
                        pass
                    else:
                        if i == 1:
                            available_throws.clear()
                        for j in range(min_Col,max_Col+1):
                            available_throws.append((line, j))
            
            ## Update opponent throws
            id = getattr(self, "oppo") 
            throw = getattr(self, "oppo_throw_remain")
            available_throws = getattr(self, "available_oppo_throws")


    def generate_best_action(self):
        
        # Kill directly
        possible_ally_actions = []
        if self.ally_throw_remain > 2:
            for piece in self.board[self.oppo]:
                if piece[1] in self.available_ally_throws:
                    if piece[0] == 'r':
                        possible_ally_actions.append(("THROW", "p", (piece[1])))
                    elif piece[0] == 'p':
                        possible_ally_actions.append(("THROW", "s", (piece[1])))
                    else:
                        possible_ally_actions.append(("THROW", "r", (piece[1])))



        print(possible_ally_actions)
        if len(possible_ally_actions) > 0:
            print(possible_ally_actions)
        if len(possible_ally_actions) == 0:
            possible_ally_actions = self.get_actions("ally")

        possible_oppo_actions = self.get_actions("oppo")

        print(self.available_oppo_throws)

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
                
                # 一个function 解决： 返回Expected Value( 和 Matrix)
                # board.futhre_board(times, throw, throw) 
                # 
                # Function in board 
                # temp_array.append(board.futhre_board());
                temp_array.append(board.evaluation(self))
            
            matrix.append(temp_array)

        # matrix [possible action] [oppo action]

        list_res , expect = gt.solve_game(matrix)
        max_score = max(list_res)



        best_action = possible_ally_actions[list(list_res).index(max_score)]

        return best_action


    def get_actions(self, id):
    
        possible_throw_actions = []
        possible_move_actions = []

        if id == "ally":
            throw_remain = self.ally_throw_remain
        elif id == "oppo":
            throw_remain = self.oppo_throw_remain

        if throw_remain > 0:
            possible_throw_actions = self.get_throws(id)

            
        all_token = self.board[getattr(self, id)]

        for i in all_token:
            action_list = game.move(self, i, id)
            slide_move = game.slide(i)
            for index in action_list:
                if index in slide_move and ("SLIDE", index, i[1]) != self.last_position: 
                    possible_move_actions.append(("SLIDE", (i[1]), index))
                elif index not in slide_move and ("SWING", index, i[1]) != self.last_position:
                    possible_move_actions.append(("SWING", (i[1]), index))
                else:
                    print(("SLIDE", index, i[1]), self.last_position)
                    pass

        

        current_index = []
        for piece in self.board[self.ally]:
            current_index.append(piece[1])

        for action in possible_move_actions:
            if action[2] in current_index:
                possible_move_actions.remove(action)
        
        for action in possible_throw_actions:
            if action[2] in current_index:
                possible_throw_actions.remove(action)


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
            # print(current_type_ally)
            # print(current_type_oppo)
            if ('r' in current_type_oppo and 'p' in current_type_ally) or 'r' not in current_type_oppo:
                wanted_type.remove('p')
            if ('s' in current_type_oppo and 'r' in current_type_ally) or 's' not in current_type_oppo:
                wanted_type.remove('r')
            if ('p' in current_type_oppo and 's' in current_type_ally) or 'p' not in current_type_oppo:
                wanted_type.remove('s')

 
            if len(wanted_type) == 0 and len(current_type_oppo)== 0:
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


            if len(wanted_type) == 0 and len(current_type_oppo)== 0:
                wanted_type = self.type
        
        for i in wanted_type:
            for j in available_throws:
                possible_throws.append(("THROW",i,j))
        
        return possible_throws