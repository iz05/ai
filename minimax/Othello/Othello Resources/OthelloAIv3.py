import sys
import time

# implements alpha-beta pruning
# improved heuristic 

CORNERS = {
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

SQUARE_VALUES = {
    0 : 20,
    1 : 9,
    2 : 8, 
    3 : 8,
    4 : 8,
    5 : 8,
    6 : 9,
    7 : 20,
    8 : 9,
    9 : 9,
    10 : 6,
    11 : 6,
    12 : 6,
    13 : 6,
    14 : 9,
    15 : 9,
    16 : 8,
    17 : 6,
    18 : 4,
    19 : 4,
    20 : 4,
    21 : 4,
    22 : 6,
    23 : 8,
    24 : 8,
    25 : 6,
    26 : 4,
    27 : 2,
    28 : 2,
    29 : 4,
    30 : 6,
    31 : 8,
    32 : 8,
    33 : 6,
    34 : 4,
    35 : 2,
    36 : 2,
    37 : 4,
    38 : 6,
    39 : 8,
    40 : 8,
    41 : 6,
    42 : 4,
    43 : 4,
    44 : 4,
    45 : 4,
    46 : 6,
    47 : 8,
    48 : 9,
    49 : 9,
    50 : 6,
    51 : 6,
    52 : 6,
    53 : 6,
    54 : 9,
    55 : 9,
    56 : 20,
    57 : 9,
    58 : 8, 
    59 : 8,
    60 : 8,
    61 : 8,
    62 : 9,
    63 : 20
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
    a = 1 # weight for mobility_count_heuristic
    b = 10 # weight for diff_corner heuristic
    x_count = 0
    o_count = 0
    edge_squares = 0

    edge_squares_2 = 0

    for i in range(0, len(board)): # calculating the number of x and o
        char = board[i]
        if char == "x":
            x_count += 1
            # if SQUARE_VALUES[i] == 9 and board[CORNERS[i]] == ".":
            #     edge_squares -= 1
            # elif SQUARE_VALUES[i] == 8:
            #     edge_squares_2 += 1
            if SQUARE_VALUES[i] == 9 or SQUARE_VALUES[i] == 8:
                edge_squares_2 += 1
        elif char == "o":
            o_count += 1
            # if SQUARE_VALUES[i] == 9 and board[CORNERS[i]] == ".":
            #     edge_squares += 1
            # elif SQUARE_VALUES[i] == 8:
            #     edge_squares_2 -= 1
            if SQUARE_VALUES[i] == 9 or SQUARE_VALUES[i] == 8:
                edge_squares_2 -= 1
    board_fill = (x_count + o_count) / 64
    diff_count = x_count - o_count
    
    if board_fill == 1: # board is filled
        return 100000 * diff_count

    mobility = len(possible_moves(board, "x")) - len(possible_moves(board, "o")) # calculating mobility
    
    corners = [0, 7, 56, 63]
    x_corner = 0
    o_corner = 0
    for c in corners:
        if board[c] == "x":
            x_corner += 1
        elif board[c] == "o":
            o_corner += 1
    diff_corner = x_corner - o_corner # corner heuristic

    # heuristic = mobility * (1 - 0.2 * board_fill) + 0.2 * board_fill * diff_count + 10 * diff_corner + 2 * edge_squares_2
    heuristic = mobility + 5 * edge_squares_2 + 10 * diff_corner
    
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