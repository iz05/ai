import sys
import time

# implements alpha-beta pruning
# implements negascout
# basic heuristic 

EDGES = {
    1 : 0,
    8 : 0,
    9 : 0,
    6 : 7,
    14 : 7,
    15 : 7,
    48 : 56,
    49 : 56,
    57 : 56,
    54 : 63,
    55 : 63,
    62 : 63,
}

CORNERS = {0, 7, 56, 63}

TOKEN_SWITCH = {
    "x" : "o",
    "o" : "x",
}

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

def find_next_move(board, player, depth):
    # Based on whether player is x or o, start an appropriate version of minimax
    # that is depth-limited to "depth".  Return the best available move.
    # if player == "x":
    #     return max_step(board, depth, -100000000, 100000000)[1]
    # elif player == "o":
    #     return min_step(board, depth, -100000000, 100000000)[1]
    # else:
    #     print("Error in find_next_move method.")
    return negascout(board, depth, -100000000, 100000000, player)[1]

def max_step(board, depth, alpha, beta): # only alpha updates here
    # returns (max_value, move)
    if depth == 0: # no more moves
        return (score(board), -1)
    states = []
    moves = possible_moves(board, "x")
    if len(moves) == 0:
        return (min_step(board, depth - 1, alpha, beta), -1)
    for move in moves:
        temp_board = make_move(board, "x", move)
        sc = min_step(temp_board, depth - 1, alpha, beta)[0]

        # alpha beta pruning
        alpha = max(alpha, sc)
        if alpha >= beta:
            return (sc, move)

        states.append((sc, move))
    return max(states)
    
def min_step(board, depth, alpha, beta):
    # returns (min_value, move)
    if depth == 0: # no more moves
        return (score(board), -1)
    states = []
    moves = possible_moves(board, "o")
    if len(moves) == 0:
        return (max_step(board, depth - 1, alpha, beta), -1)
    for move in moves:
        temp_board = make_move(board, "o", move)
        sc = max_step(temp_board, depth - 1, alpha, beta)[0]

        # alpha beta pruning
        beta = min(beta, sc)
        if alpha >= beta:
            return (sc, move)

        states.append((sc, move))
    return min(states)

def negascout(board, depth, alpha, beta, token):
    if depth == 0:
        return (score(board), -1)
    # states = []
    moves = possible_moves(board, token)

    if len(moves) == 0:
        return (-1 * negascout(board, depth - 1, -1 * beta, -1 * alpha, TOKEN_SWITCH[token]), -1)
    
    count = 0
    b = beta
    best_move = -1
    for move in moves:
        temp_board = make_move(board, token, move)
        sc = -1 * negascout(temp_board, depth - 1, -1 * b, -1 * alpha, TOKEN_SWITCH[token])[0]
    
        if sc > alpha and sc < beta and count == 0:
            count += 1
            sc = -1 * negascout(temp_board, depth - 1, -1 * beta, -1 * alpha, TOKEN_SWITCH[token])[0]
        
        if sc > alpha:
            best_move = move
            alpha = sc

        if alpha >= beta:
            return (alpha, move)
        
        b = alpha + 1
        # states.append((sc, move))
        
    return (alpha, best_move)

# All your other functions
def score(board): # returns the score for a board
    x_count = 0
    o_count = 0

    score = 0

    for i in range(0, len(board)): # calculating the number of x and o
        char = board[i]
        if char == "x":
            x_count += 1
            if i in CORNERS:
                score += 500
            elif i in EDGES:
                if board[EDGES[i]] == "x" or board[EDGES[i]] == "o":
                    score += 20
                else:
                    score -= 20
        elif char == "o":
            o_count += 1
            if i in CORNERS:
                score -= 500
            elif i in EDGES:
                if board[EDGES[i]] == "x" or board[EDGES[i]] == "o":
                    score -= 20
                else:
                    score += 20

    x_moves = len(possible_moves(board, "x"))
    o_moves = len(possible_moves(board, "o")) # calculating mobility
    
    if x_moves == 0 and o_moves == 0 or x_count + o_count == 64: # board is filled
        return 100000000 * (x_count - o_count) / (x_count + o_count)
    
    score += x_moves - o_moves

    return score


board = sys.argv[1]
player = sys.argv[2]
depth = 1

for count in range(board.count(".")):  # No need to look more spaces into the future than exist at all
    print(find_next_move(board, player, depth))
    depth += 1

# class Strategy():
#    logging = True  # Optional
#    def best_strategy(self, board, player, best_move, still_running):
#        depth = 1
#        for count in range(board.count(".")):  # No need to look more spaces into the future than exist at all
#            best_move.value = find_next_move(board, player, depth)
#            depth += 1

# results = []
# with open("boards_timing.txt") as f:
#     for line in f:
#         board, token = line.strip().split()
#         temp_list = [board, token]
#         print(temp_list)
#         for count in range(1, 7):
#             print("depth", count)
#             start = time.perf_counter()
#             find_next_move(board, token, count)
#             end = time.perf_counter()
#             temp_list.append(str(end - start))
#         print(temp_list)
#         print()
#         results.append(temp_list)
# with open("boards_timing_my_results.csv", "w") as g:
#     for l in results:
#         g.write(", ".join(l) + "\n")