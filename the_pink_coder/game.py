def move(board, index, id):
    
    action_list = []
    list_1 = slide(index)
    list_2 = swing(board, index, id)
    tot_list = []

    tot_list += list_1
    
    # Extract list elements from list_2
    for list in list_2:
        tot_list += list

    # Check duplicate indexes
    for i in tot_list:
        if i not in action_list:
            action_list.append(i)

    return action_list


def swing(board, index, id):
    
    possible_trans_index = slide(index)
    trans_index = []
    result_pieces = []
    
    for i in board.board[getattr(board, id)]:
        if i[1] in possible_trans_index:
            trans_index.append(i)
    

    for i in trans_index:
        slide_move = slide(i)
        # Remove index itself
        if index[1] in slide_move:
            slide_move.remove(index[1])
        result_pieces.append(slide_move)
        
    return result_pieces


def slide(index):
    
    row = index[1][0]
    col = index[1][1]

    original_index = (row, col)
    possible_result_coord = [(row + 1, col - 1), (row + 1, col), (row, col - 1), (row, col + 1), (row - 1, col), (row - 1, col + 1)]

    result_pieces = []

    for i in possible_result_coord:
        if not out_boundary(i):
            result_pieces.append(i)

    return result_pieces


def out_boundary(coord):
       
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


# RoPaSci combat rule
def defeat(piece_1, piece_2):
    # If two piece are on the same spot
    if same_coord(piece_1, piece_2):
        if ((piece_1[0] == 'r') and (piece_2[0] == 's')) or ((piece_1[0] == 's') and (piece_2[0] == 'p')) or ((piece_1[0] == 'p') and (piece_2[0] == 'r')):
            return True 
        elif ((piece_1[0] == 'r') and (piece_2[0] == 'p')) or ((piece_1[0] == 's') and (piece_2[0] == 'r')) or ((piece_1[0] == 'p') and (piece_2[0] == 's')):
            return False
        elif ((piece_1[0] == 'r') and (piece_2[0] == 'r')) or ((piece_1[0] == 'p') and (piece_2[0] == 'p')) or ((piece_1[0] == 's') and (piece_2[0] == 's')):
            return False
        else:
            return False
    else:
        return False


def defeat_score(type_1, type_2, factor=1):
    if ((type_1 == 'r') and (type_2 == 's')) or ((type_1 == 's') and (type_2 == 'p')) or ((type_1 == 'p') and (type_2 == 'r')):
        return 1*factor
    elif ((type_1 == 'r') and (type_2 == 'p')) or ((type_1 == 's') and (type_2 == 'r')) or ((type_1== 'p') and (type_2 == 's')):
        return -1*factor
    elif ((type_1 == 'r') and (type_2 == 'r')) or ((type_1 == 'p') and (type_2 == 'p')) or ((type_1 == 's') and (type_2 == 's')):
        return 0

 
# Get coordinates from one piece, piece = ('r',(0,1))
def get_coord(piece):
    return (piece[1][0], piece[1][1])


# Check if two pieces at same spot
def same_coord(piece_1, piece_2):
    if get_coord(piece_1)[0] == get_coord(piece_2)[0] and get_coord(piece_1)[1] == get_coord(piece_2)[1]:
        return True
    else:
        return False