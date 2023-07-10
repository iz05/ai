import sys
from othello_imports import make_move, possible_moves

def find_next_move(board, player, depth):
    # Based on whether player is x or o, start an appropriate version of minimax
    # that is depth-limited to "depth".  Return the best available move.
    if player == "x":
        return max_step(board, depth)[1]
    elif player == "o":
        return min_step(board, depth)[1]
    else:
        print("Error in find_next_move method.")

def max_step(board, depth):
    # returns (max_value, move)
    if depth == 0: # no more moves
        return (score(board), -1)
    states = []
    moves = possible_moves(board, "x")
    if len(moves) == 0:
        return (score(board), -1)
    for move in moves:
        temp_board = make_move(board, "x", move)
        sc = min_step(temp_board, depth - 1)[0]
        states.append((sc, move))
    return max(states)
    

def min_step(board, depth):
    # returns (min_value, move)
    if depth == 0: # no more moves
        return (score(board), -1)
    states = []
    moves = possible_moves(board, "o")
    if len(moves) == 0:
        return (score(board), -1)
    for move in moves:
        temp_board = make_move(board, "o", move)
        sc = max_step(temp_board, depth - 1)[0]
        states.append((sc, move))
    return min(states)

# All your other functions
def score(board): # returns the score for a board and token
    a = 1 # weight for mobility_count_heuristic
    b = 10 # weight for diff_corner heuristic
    x_count = 0
    o_count = 0

    for char in board: # calculating the number of x and o
        if char == "x":
            x_count += 1
        elif char == "o":
            o_count += 1
    board_fill = (x_count + o_count) / 64
    
    if board_fill == 1: # board is filled
        return 100000000 * (x_count - o_count)

    diff_count = x_count - o_count
    mobility = len(possible_moves(board, "x")) - len(possible_moves(board, "o")) # calculating mobility
    mobility_count_heuristic = board_fill  * diff_count + (1 - board_fill) * 10 * mobility # weighting mobility and difference in count for a heuristic

    corners = [0, 7, 56, 63]
    x_corner = 0
    o_corner = 0
    for c in corners:
        if board[c] == "x":
            x_corner += 1
        elif board[c] == "o":
            o_corner += 1
    diff_corner = x_corner - o_corner # corner heuristic

    heuristic = a * mobility_count_heuristic + b * diff_corner
    return heuristic


board = sys.argv[1]
player = sys.argv[2]
depth = 1

for count in range(board.count(".")):  # No need to look more spaces into the future than exist at all
    print(find_next_move(board, player, depth))
    depth += 1