directions = [-11, -10, -9, -1, 1, 9, 10, 11] # the 8 different directions (left, right, up, down, and the 4 diagonal directions)

def possible_moves(board, token):
    board = make_border(board)
    moves = []
    for index in range(0, 100):
        if board[index] == ".": # possible to place the token
            move_possible = False
            for dir in directions: # check every direction, if at least one works, then this move is allowed
                if check_move_in_direction(board, token, index, dir):
                    move_possible = True
                    break
            if move_possible:
                moves.append(convert_index_to_64(index))
    return moves

def make_move(board, token, index):
    board = make_border(board)
    new_index = convert_index_to_100(index)
    flip_indices = set()
    for dir in directions:
        data = move_in_direction(board, token, new_index, dir)
        if type(data) == set:
            flip_indices.update(data)
    board = remove_border(board)
    new_board = ""
    for i in range(0, len(board)):
        if i in flip_indices or i == index:
            new_board += token
        else:
            new_board += board[i]
    return new_board
        

def make_border(board): # adds question mark border
    new_board = "??????????"
    for i in range(0, 64, 8):
        new_board += "?" + board[i : i + 8] + "?"
    new_board += "??????????"
    return new_board

def remove_border(board): # removes question mark border
    new_board = ""
    for i in range(11, 91, 10):
        new_board += board[i : i + 8]
    return new_board

def convert_index_to_64(ind): # converts index from the 100-board to the resulting index in the 64-board
    row = ind // 10
    return ind - (2 * row - 1) - 10

def convert_index_to_100(ind): # converts index from the 64-board to the resulting index in the 100-board
    row = ind // 8
    return ind + (2 * row + 1) + 10

def check_move_in_direction(board, token, index, dir):
    cur_index = index + dir
    count = 0
    while board[cur_index] != "?" and board[cur_index] != ".":
        if board[cur_index] == token and count == 0:
            return False
        elif board[cur_index] == token:
            return True
        cur_index += dir
        count += 1
    return False

def move_in_direction(board, token, index, dir): # same as check_move_in_direction except returns indices (of 64-board) that should be flipped
    cur_index = index + dir
    count = 0
    indices = set()
    while board[cur_index] != "?" and board[cur_index] != ".":
        if board[cur_index] == token and count == 0:
            return False
        elif board[cur_index] == token:
            return indices
        indices.add(convert_index_to_64(cur_index))
        cur_index += dir
        count += 1
    return False