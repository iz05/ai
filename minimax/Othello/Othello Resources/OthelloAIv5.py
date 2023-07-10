import sys
import time

# implements alpha-beta pruning
# improved heuristic 

# version completed 11/9 at 11:58 am
# do not change

CORNERS = {
    0 : {1, 8, 9},
    7 : {6, 14, 15},
    56 : {48, 49, 57},
    63: {54, 55, 62}
}

SQUARE_VALUES = {
    0 : 100,
    1 : -10,
    2 : 11, 
    3 : 6,
    4 : 6,
    5 : 11,
    6 : -10,
    7 : 100,
    8 : -10,
    9 : -20,
    10 : 1,
    11 : 2,
    12 : 2,
    13 : 1,
    14 : -20,
    15 : -10,
    16 : 10,
    17 : 1,
    18 : 5,
    19 : 4,
    20 : 4,
    21 : 5,
    22 : 1,
    23 : 10,
    24 : 6,
    25 : 2,
    26 : 4,
    27 : 2,
    28 : 2,
    29 : 4,
    30 : 2,
    31 : 6,
    32 : 6,
    33 : 2,
    34 : 4,
    35 : 2,
    36 : 2,
    37 : 4,
    38 : 2,
    39 : 6,
    40 : 10,
    41 : 1,
    42 : 5,
    43 : 4,
    44 : 4,
    45 : 5,
    46 : 1,
    47 : 10,
    48 : -10,
    49 : -20,
    50 : 1,
    51 : 2,
    52 : 2,
    53 : 1,
    54 : -20,
    55 : -10,
    56 : 100,
    57 : -10,
    58 : 11, 
    59 : 6,
    60 : 6,
    61 : 11,
    62 : -10,
    63 : 100
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
    if player == "x":
        return max_step(board, depth, -100000000, 100000000)[1]
    elif player == "o":
        return min_step(board, depth, -100000000, 100000000)[1]
    else:
        print("Error in find_next_move method.")

def max_step(board, depth, alpha, beta): # only alpha updates here
    # returns (max_value, move)
    if depth == 0: # no more moves
        return (score(board), -1)
    states = []
    moves = possible_moves(board, "x")
    if len(moves) == 0:
        return (score(board), -1)
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
        return (score(board), -1)
    for move in moves:
        temp_board = make_move(board, "o", move)
        sc = max_step(temp_board, depth - 1, alpha, beta)[0]

        # alpha beta pruning
        beta = min(beta, sc)
        if alpha >= beta:
            return (sc, move)

        states.append((sc, move))
    return min(states)

# All your other functions
def score(board): # returns the score for a board and token
    x_count = 0
    o_count = 0
    weighted_count = 0

    for i in range(0, len(board)): # calculating the number of x and o
        char = board[i]
        if char == "x":
            x_count += 1
            weighted_count += SQUARE_VALUES[i]
            if SQUARE_VALUES[i] == 100:
                for val in CORNERS[i]:
                    SQUARE_VALUES[val] *= -1
        elif char == "o":
            o_count += 1
            weighted_count -= SQUARE_VALUES[i]
            if SQUARE_VALUES[i] == 100:
                for val in CORNERS[i]:
                    SQUARE_VALUES[val] *= -1
                    
    board_fill = (x_count + o_count) / 64
    diff_count = x_count - o_count
    
    if board_fill == 1: # board is filled
        return 100000 * diff_count

    mobility = len(possible_moves(board, "x")) - len(possible_moves(board, "o")) # calculating mobility

    # if x_count + o_count <= 14: # beginning of game
    #     heuristic = weighted_count
    # elif x_count + o_count <= 40: # middle of game
    #     heuristic = mobility * 5 + weighted_count
    # elif x_count + o_count <= 60: # near the end of the game
    #     heuristic = weighted_count
    # else:
    #     heuristic = x_count - o_count
    heuristic = 5 * mobility * (1 - board_fill) + board_fill * weighted_count # used for othello server
    return heuristic


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