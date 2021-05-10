import math
import the_pink_coder.game as game
from copy import deepcopy
import the_pink_coder.gametheory as gt
import numpy as np
import random

class Board:
    
    # Initialize the board
    def __init__(self, ally, oppo, board={"upper": [], "lower": []}):
        self.ally = ally
        self.oppo = oppo
        self.board = board
        self.available_ally_throws = []
        self.available_oppo_throws = []
        self.possible_ally_throws = []
        self.possible_oppo_throws = []
        self.ally_index = []
        self.protected = True
        self.ally_throw_remain = 9
        self.oppo_throw_remain = 9
        self.type = ["r", "p", "s"]
        self.all_index = {4: (-4, 0), 3: (-4, 1), 2: (-4, 2), 1: (-4, 3), 0: (-4, 4), -1: (-3, 4), -2: (-2, 4), -3: (-1, 4), -4: (0, 4)}
        self.last_position = ()
        self.round = 0
        if self.ally == "lower":
            self.limit_list = [4,3,2,1,0]
        else:
            self.limit_list = [-4,-3,-2,-1,0]

    # Update Board function
    def update_board(self, oppo_action, ally_action, printRes):

        # Keep track of the data the board needed
        self.round+=1
        if ally_action[0] == "THROW":
            self.ally_throw_remain -= 1
        if oppo_action[0] == "THROW":
            self.oppo_throw_remain -= 1
        if self.oppo_throw_remain < 4 or self.round > 10:
            self.protected = False

        # Start to update, start from ally action
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
        
        # Update the opponent action
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
        
        # Update combat result, decide which token is left in those coordinate
        tokens = self.board["upper"] + self.board["lower"]
        for i in tokens:
            for j in self.board["upper"]:
                if game.same_coord(i, j) and game.defeat(i, j):
                    self.board["upper"].remove(j)

            for k in self.board["lower"]:
                if game.same_coord(i, k) and game.defeat(i, k):
                    self.board["lower"].remove(k)

        self.update_available_throw()

    # Update the throw both player and opponent could throw in each turn
    def update_available_throw(self):
        # Update ally throws
        id = getattr(self, "ally") 
        throw = getattr(self, "ally_throw_remain")
        available_throws = getattr(self, "available_ally_throws")
        possible_throws = getattr(self, "possible_ally_throws")

        # Updating the avaliable throw choice based on it is upper player 
        # or lower player
        for i in range (0, 2, 1):
            if throw > 0:
                if id == "upper":
                    line = 4 - (9 - throw)
                    min_Col = self.all_index[line][0]
                    max_Col = self.all_index[line][1]
                    available_throws.clear()
                    if (line, min_Col) in available_throws:
                        pass
                    else:
                        for j in range(min_Col,max_Col+1):
                            available_throws.append((line, j))
                            possible_throws.append((line, j))
                        
                else:
                    line = -4 + (9 - throw)
                    min_Col = self.all_index[line][0]
                    max_Col = self.all_index[line][1]
                    available_throws.clear()
                    if (line, min_Col) in available_throws:
                        pass
                    else:
                        for j in range(min_Col,max_Col+1):
                            available_throws.append((line, j))
                            possible_throws.append((line, j))
            
            ## Update opponent throws
            id = getattr(self, "oppo") 
            throw = getattr(self, "oppo_throw_remain")
            available_throws = getattr(self, "available_oppo_throws")
            possible_throws = getattr(self, "possible_oppo_throws")


    # Generate the best action out player could do based on current situation
    def generate_best_action(self, multi=True):
        possible_ally_actions = self.get_actions_ally()
        possible_oppo_actions = self.get_actions_oppo()

        # print(possible_ally_actions)
        # print(possible_oppo_actions)

        # Based on ally's action and opponent's action, create a pay-off matrix
        # regarding ally's action and opponent's action
        matrix = []
        for ally_action in possible_ally_actions:
            temp_array = []
            for oppo_action in possible_oppo_actions:
                board = deepcopy(self)
                board.update_board(oppo_action, ally_action, False)
                temp_array.append(board.evaluation(self))
            
            matrix.append(temp_array)

        list_res, expect = gt.solve_game(matrix)
        # While it is in multi stage mode, it would look further of the action
        # pair, have an insight of the future status
        if multi == True and len(list_res) >= 2:
            possible_ally_actions_2 = []
            # Median
            median_score = np.percentile(list_res, 50)
            for ally_action_score in list_res:
                if ally_action_score > median_score:
                    best_action_2 = possible_ally_actions[list(list_res).index(ally_action_score)]
                    possible_ally_actions_2.append(best_action_2)
            
            matrix_2 = []
            for ally_action in possible_ally_actions_2:   
                temp_array = []
                flag = 0
                for oppo_action in possible_oppo_actions:
                    if flag%3 == 0:
                        board = deepcopy(self)
                        board.update_board(oppo_action, ally_action, False)
                        temp_array.append(board.multi_stage())
                    flag += 1
                matrix_2.append(temp_array)

            list_res_2, expect = gt.solve_game(matrix_2)
            max_score_2 = max(list_res_2)
            best_action = possible_ally_actions_2[list(list_res_2).index(max_score_2)]

        # Single-stage
        else:
            size = len(possible_ally_actions)
            index = np.random.choice(np.arange(size), p = list(list_res))
            best_action = possible_ally_actions[index]
        
        return best_action

    # Evaluation function for each board
    def evaluation(self, old_board):   
        
        score = 0

        # Calculating the distance score, basically is on how far of ally token
        # from the opponent token which it could defeat and the opponent which 
        # could defeated it
        distance_score = 0
        for i in self.board[self.ally]:
            min_defeated = 0
            max_defeated = 0
            for j in self.board[self.oppo]: 
                current_score = self.defeat_score(i[0], j[0], (12 - self.distance(i, j)))
                if current_score < 0 and current_score < max_defeated:
                    max_defeated = current_score
                elif current_score > 0 and current_score > min_defeated:
                    min_defeated = current_score

            distance_score += max_defeated
            distance_score += min_defeated

        if len(self.board[self.ally]) > 0:
            distance_score = distance_score / len(self.board[self.ally])

        # Compare the difference of amount of ally token and opponent token
        diff_ally = len(old_board.board[self.ally]) - len(self.board[self.ally])
        diff_oppo = len(old_board.board[self.oppo]) - len(self.board[self.oppo])


        # Assign weight to different feature and 
        score = 1.5 * distance_score - 12 * diff_ally + 20 * diff_oppo

        return score

    # Helper function for evaluating the board status
    def defeat_score(self, type_1, type_2, factor):
        if ((type_1 == 'r') and (type_2 == 's')) or ((type_1 == 's') and (type_2 == 'p')) or ((type_1 == 'p') and (type_2 == 'r')):
            return 1.55 * factor
        elif ((type_1 == 'r') and (type_2 == 'p')) or ((type_1 == 's') and (type_2 == 'r')) or ((type_1== 'p') and (type_2 == 's')):
            return -0.77 * factor
        elif ((type_1 == 'r') and (type_2 == 'r')) or ((type_1 == 'p') and (type_2 == 'p')) or ((type_1 == 's') and (type_2 == 's')):
            return 0

    # Helper function for calculating the distance of two status
    def distance(self, piece_1, piece_2):
        coord_1 = game.get_coord(piece_1)
        coord_2 = game.get_coord(piece_2)
        return math.sqrt(pow(coord_1[0] - coord_2[0], 2) + pow(coord_1[1] - coord_2[1], 2))

    # Generate the potential good throw of ally, which could kill opponent 
    # directly
    def generate_action_ally(self):
        ally_dict = {"r":0,"p":0,"s":0}
        for peice in self.board[self.ally]:
            ally_dict[peice[0]] += 1

        # Figure out any directly kill throw
        possible_ally_actions = []
        remain_oppo = len(self.board[self.oppo]) + self.oppo_throw_remain
        if self.ally_throw_remain > 2:
            for piece in self.board[self.oppo]:
                if piece[1] in self.possible_ally_throws:
                    if (piece[0] == 'r' and (ally_dict["p"]+1)/(len(self.board[self.ally])+1) <= 0.6) or (piece[0] == 'r' and remain_oppo <= 3):
                        possible_ally_actions.append(("THROW", "p", (piece[1])))
                    elif (piece[0] == 'p' and (ally_dict["s"]+1)/(len(self.board[self.ally])+1) <= 0.6) or (piece[0] == 'p' and remain_oppo <= 3):
                        possible_ally_actions.append(("THROW", "s", (piece[1])))
                    elif (piece[0] == 's' and (ally_dict["r"]+1)/(len(self.board[self.ally])+1) <= 0.6) or (piece[0] == 's' and remain_oppo <= 3):
                        possible_ally_actions.append(("THROW", "r", (piece[1])))

        if len(possible_ally_actions) > 0:
            percentage = 1 - (1 / len(self.board[self.oppo]))
            if percentage >= 0.5:
                pass
            elif remain_oppo < 4:
                pass
            else: 
                possible_ally_actions = []

        return possible_ally_actions

    # Generate the potential great action for opponent, which to kill tha ally
    # directly
    def generate_action_oppo(self):
        ally_dict = {"r":0,"p":0,"s":0}
        for peice in self.board[self.oppo]:
            ally_dict[peice[0]] += 1

        possible_ally_actions = []
        remain_oppo = len(self.board[self.ally]) + self.ally_throw_remain
        if self.oppo_throw_remain > 0:
            for piece in self.board[self.ally]:
                if piece[1] in self.possible_oppo_throws:
                    if (piece[0] == 'r' and (ally_dict["p"]+1) /(len(self.board[self.oppo])+1) <= 0.5) or (piece[0] == 'r' and remain_oppo <= 2):
                        possible_ally_actions.append(("THROW", "p", (piece[1])))
                    elif (piece[0] == 'p' and (ally_dict["s"]+1) /(len(self.board[self.oppo])+1) <= 0.5) or (piece[0] == 'p' and remain_oppo <= 2):
                        possible_ally_actions.append(("THROW", "s", (piece[1])))
                    elif (piece[0] == 's' and (ally_dict["r"]+1) /(len(self.board[self.oppo])+1) <= 0.5) or (piece[0] == 's' and remain_oppo <= 2):
                        possible_ally_actions.append(("THROW", "r", (piece[1])))
        if len(possible_ally_actions) > 0:
            percentage = 1 - (1 / len(self.board[self.ally]))
            if percentage >= 0.5:
                pass
            elif remain_oppo < 3:
                pass
            else: 
                possible_ally_actions = []

        return possible_ally_actions

    # Generate all ally's action, may include throw and move(slide, swing)
    def get_actions_ally(self):
        
        possible_throw_actions = []
        possible_move_actions = []

        all_action = self.generate_action_ally()
        if all_action != []:
            return all_action

        throw_remain = self.ally_throw_remain
        oppo_id = "oppo"
        possible_move_actions = self.get_move_ally()

        if throw_remain > 0:
            possible_throw_actions = self.get_throws("ally")

        # Prevent two out token in same column, it is dangerous and may kill
        # ourselves
        current_index = []
        for piece in self.board[self.ally]:
            current_index.append(piece[1])

        for action in possible_move_actions:
            if action[2] in current_index:
                possible_move_actions.remove(action)
        
        for action in possible_throw_actions:
            if action[2] in current_index:
                possible_throw_actions.remove(action)
        all_action = possible_move_actions + possible_throw_actions
        return all_action

    # Generate all opponent's action, including throw, move(slide, swing)
    def get_actions_oppo(self):
        
        possible_throw_actions = []
        possible_move_actions = []

        all_action = self.generate_action_oppo()
        if all_action != []:
            return all_action

        throw_remain = self.oppo_throw_remain
        oppo_id = "ally"
        possible_move_actions = self.get_move_oppo()

        if throw_remain > 0:
            possible_throw_actions = self.get_throws("oppo")

        return possible_move_actions + possible_throw_actions

    # Get all the move actin of the opponent player
    def get_move_oppo(self):
        ally_token = self.board[self.oppo]
        dict = {"r": 12, "p":12,"s":12}
        dict_piece = {}
        moveable = []
        possible_move_actions = []

        # Find it there is any token which is "efficient", which means it is
        # really close to the opponent token which it could kill or really close 
        # to the token which could kill it,(it should run away)
        for i in ally_token:
            flag = 0
            for oppo in self.board[self.ally]:
                if game.defeat(i, oppo) and self.distance(i, oppo) < dict[i[0]]:
                    dict[i[0]] = self.distance(i, oppo)
                    dict_piece[i[0]] = i 
                # Emergency
                if flag == 0 and game.defeat(oppo, i) and self.distance(i, oppo) < 1:
                    moveable.append(i)
                    flag = 1

        for atype in dict_piece:
            moveable.append(dict_piece[atype])

        if len(moveable) == 0:
            moveable = ally_token

        # Create move for all "efficient" token
        for piece in moveable:
            action_list = game.move(self, piece, "oppo")
            slide_move = game.slide(piece)
            for index in action_list:
                if index in slide_move and ("SLIDE", index, piece[1]): 
                    possible_move_actions.append(("SLIDE", (piece[1]), index))
                elif index not in slide_move and ("SWING", index, piece[1]):
                    possible_move_actions.append(("SWING", (piece[1]), index))
                else:
                    pass

        return possible_move_actions


    def get_move_ally(self):
        ally_token = self.board[self.ally]
        oppo_id = "oppo"
        dict = {"r": 12, "p":12,"s":12}
        dict_piece = {}
        moveable = []
        possible_move_actions = []
        # Find it there is any token which is "efficient", which means it is
        # really close to the opponent token which it could kill or really close 
        # to the token which could kill it,(it should run away)
        for i in ally_token:
            flag = 0
            for oppo in self.board[self.oppo]:
                if game.defeat(i, oppo) and self.distance(i, oppo) < dict[i[0]]:
                    dict[i[0]] = self.distance(i, oppo)
                    dict_piece[i[0]] = i 
                # Emergency
                if flag == 0 and game.defeat(oppo, i) and self.distance(i, oppo) <= 1:
                    moveable.append(i)
                    flag = 1

        for atype in dict_piece:
            moveable.append(dict_piece[atype])

        if len(moveable) == 0:
            moveable = ally_token
        for piece in moveable:
            action_list = game.move(self, piece, "ally")
            slide_move = game.slide(piece)
            for index in action_list:
                if (self.protected == True and index[0] in self.limit_list):
                    possible_move_actions = possible_move_actions
                else:
                    if index in slide_move and ("SLIDE", index, piece[1]) != self.last_position: 
                        possible_move_actions.append(("SLIDE", (piece[1]), index))
                    elif index not in slide_move and ("SWING", index, piece[1]) != self.last_position:
                        possible_move_actions.append(("SWING", (piece[1]), index))
                    else:
                        pass

        return possible_move_actions
        
    # Get throw on particular player, based on current throw situation
    def get_throws(self, id):
        def get_throws(self, id):
            possible_throws = []
        
        if id == "ally":
            available_throws = self.available_ally_throws
            ally_token = self.board[self.ally]
            oppo_token = self.board[self.oppo]
            oppo_remain_throw = self.oppo_throw_remain
        elif id == "oppo":
            available_throws = self.available_oppo_throws
            ally_token = self.board[self.oppo]
            oppo_token = self.board[self.ally]
            oppo_remain_throw = self.ally_throw_remain


        # Avoid unnecessary throw, figure out which type is necessary in the 
        # current situation
        wanted_type = ["r","p","s"]
        current_type_ally = []
        for piece in ally_token:
            if piece[0] not in current_type_ally:
                current_type_ally.append(piece[0])
        
        current_type_oppo = []
        for piece in oppo_token:
            if piece[0] not in current_type_oppo:
                current_type_oppo.append(piece[0])

        if ('r' in current_type_oppo and 'p' in current_type_ally) or 'r' not in current_type_oppo:
            wanted_type.remove('p')
        if ('s' in current_type_oppo and 'r' in current_type_ally) or 's' not in current_type_oppo:
            wanted_type.remove('r')
        if ('p' in current_type_oppo and 's' in current_type_ally) or 'p' not in current_type_oppo:
            wanted_type.remove('s')

        if len(wanted_type) == 0 and oppo_remain_throw == 9:
            wanted_type = self.type
        
        possible_throws = []
        for i in wanted_type:
            for j in available_throws:
                possible_throws.append(("THROW",i,j))
        random.shuffle(possible_throws)
        return possible_throws


    # Function for multi-stage section of the implementation
    def multi_stage(self):
        possible_ally_actions = self.get_actions_ally()
        possible_oppo_actions = self.get_actions_oppo()
        matrix = []
        for ally_action in possible_ally_actions:
            temp_array = []
            for oppo_action in possible_oppo_actions:
                board = deepcopy(self)
                board.update_board(oppo_action, ally_action, False)
                temp_array.append(board.evaluation(self))
            matrix.append(temp_array)
        list_res, expect = gt.solve_game(matrix)
        return expect