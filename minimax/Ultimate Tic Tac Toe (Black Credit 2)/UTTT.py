import random
import sys

values = {
    "x" : 1,
    "o" : -1,
    "." : 0,
    "t" : 0,
}

potential_wins = {
    (0, 1) : 2,
    (1, 2) : 0,
    (0, 2) : 1,
    (3, 4) : 5,
    (4, 5) : 3,
    (3, 5) : 4,
    (6, 7) : 8,
    (7, 8) : 6,
    (6, 8) : 7,
    (0, 3) : 6,
    (0, 6) : 3,
    (3, 6) : 0,
    (1, 4) : 7,
    (1, 7) : 4,
    (4, 7) : 1,
    (2, 5) : 8,
    (2, 8) : 5,
    (5, 8) : 2,
    (0, 4) : 8,
    (0, 8) : 4,
    (4, 8) : 0,
    (2, 4) : 6,
    (2, 6) : 4,
    (4, 6) : 2,
}

def print_board(board):
    for i in range(0, 3):
        for j in range(0, 3):
            print(board[3 * i][3 * j : 3 * (j + 1)] + " | " + board[3 * i + 1][3 * j : 3 * (j + 1)] + " | " + board[3 * i + 2][3 * j : 3 * (j + 1)])
        print("---------------")

def can_play(board, square): # returns true if the board is still able to be played
    return not (board[square] == "XXXXXXXXX" or board[square] == "OOOOOOOOO" or board[square] == "TTTTTTTTT") and square != -1

def check_win(board, token):
    for i in range(0, 3):
        if board[3 * i] == token and board[3 * i + 1] == token and board[3 * i + 2] == token: # check rows
            return True
        elif board[i] == token and board[i + 3] == token and board[i + 6] == token: # check columns
            return True
    if board[0] == token and board[4] == token and board[8] == token or board[2] == token and board[4] == token and board[6] == token:
        return True
    return False

def goal_state(board): # returns 1 if win, 0 if tie, -1 if neither
    new_board = ""
    for i in range(0, 9):
        if board[i] == "XXXXXXXXX":
            new_board += "x"
        elif board[i] == "OOOOOOOOO":
            new_board += "o"
        elif board[i] == "TTTTTTTTT":
            new_board += "t"
        else:
            new_board += "."

    if check_win(new_board, "x"):
        return 1
    elif check_win(new_board, "o"):
        return -1
    elif "." not in new_board:
        return 0
    return False

def sub_goal_state(board, square): # checks if token has won the board, returns 1 if x wins, 0 if tie, -1 if o wins, False if game is not done
    if check_win(board[square], "x"):
        return 1
    elif check_win(board[square], "o"):
        return -1
    elif "." not in board[square]:
        return 0
    return False

def get_possible_moves(board, square): # square is the index of the board that was just played on, returns possible moves that are made
    moves = []
    if can_play(board, square):
        for i in range(0, 9):
            if board[square][i] == ".":
                moves.append((square, i))
    else:
        for i in range(0, 9):
            if can_play(board, i):
                for j in range(0, 9):
                    if board[i][j] == ".":
                        moves.append((i, j))
    return moves


def make_move(board, move, token): # returns (new_board, index of square played on), updates the board
    square, index = move
    new_board = board.copy()
    new_board[square] = board[square][ : index] + token + board[square][index + 1 : ]
    
    val = sub_goal_state(new_board, square)
    if type(val) == int:
        if val == 1:
            new_board[square] = "XXXXXXXXX"
        elif val == 0:
            new_board[square] = "TTTTTTTTT"
        else:
            new_board[square] = "OOOOOOOOO"
    
    return (new_board, index)

def sub_score(board, square): # returns score of a normal tic tac toe board, indicates how close x or o is to winning
    val = sub_goal_state(board, square)
    if type(val) == int:
        return 10000 * val

    score = 0
    weights = [2, 1, 2, 1, 4, 1, 2, 1, 2] 
    subboard = board[square]
    for square1, square2 in potential_wins:
        square3 = potential_wins[(square1, square2)]
        if subboard[square1] == subboard[square2] and subboard[square1] != "." and subboard[square1] != "t" and subboard[square3] == ".":
            score += 1000 * values[subboard[square1]] 
    
    for i in range(0, 9):
        score += weights[i] * values[subboard[i]]
    
    return score

def score(board): # returns total score
    val = goal_state(board)
    if type(val) == int:
        return 1000000000 * val
    
    new_board = make_subboard(board)
    
    weights = get_weights(new_board)
    score = 0
    for i in range(0, 9):
        score += weights[i] * sub_score(board, i)

    return score

def make_subboard(board):
    new_board = ""
    for i in range(0, 9):
        if board[i] == "XXXXXXXXX":
            new_board += "x"
        elif board[i] == "OOOOOOOOO":
            new_board += "o"
        elif board[i] == "TTTTTTTTT":
            new_board += "t"
        else:
            new_board += "."
    return new_board

def get_weights(subboard): # returns an assignment of weights given the current configuration
    weights = [2, 1, 2, 1, 4, 1, 2, 1, 2] 
    for square1, square2 in potential_wins:
        square3 = potential_wins[(square1, square2)]
        if subboard[square1] == subboard[square2] and subboard[square1] != "." and subboard[square2] != "t" and subboard[square3] == ".":
            weights[square3] += 10
    return weights

def max_move(board, square, depth, alpha, beta): # returns (score, move)
    if depth == 0:
        return (score(board), (-1, -1))
    vals = []
    for move in get_possible_moves(board, square):
        temp_board = board.copy()
        new_board, new_square = make_move(temp_board, move, "x")
        sc = min_move(new_board, new_square, depth - 1, alpha, beta)[0]

        # alpha beta pruning
        alpha = max(alpha, sc)
        if alpha >= beta:
            return (sc, move)

        vals.append((sc, move))
    if len(vals) == 0:
        return (score(board), (-1, -1))
    return max(vals)

def min_move(board, square, depth, alpha, beta): # return (score, move)
    if depth == 0:
        return (score(board), (-1, -1))
    vals = []
    for move in get_possible_moves(board, square):
        temp_board = board.copy()
        new_board, new_square = make_move(temp_board, move, "o")
        sc = max_move(new_board, new_square, depth - 1, alpha, beta)[0]

        # alpha beta pruning
        beta = min(beta, sc)
        if alpha >= beta:
            return (sc, move)

        vals.append((sc, move))
    if len(vals) == 0:
        return (score(board), (-1, -1))
    return min(vals)

def play_game(player1, player2):
    board = ["........." for i in range(0, 9)]
    cur_player = player1
    tokens = {
        player1 : "x",
        player2 : "o"
    }
    square = -1
    while(True):
        print_board(board)
        print()
        val = goal_state(board)
        if type(val) == int:
            if val == 1:
                print("X won!")
            elif val == 0:
                print("Tie!")
            else:
                print("O won!")
            break
        move = cur_player.move(board, square, tokens[cur_player])
        board, square = make_move(board, move, tokens[cur_player])
        print("Move made by " + tokens[cur_player] + " : " + str(move))
        if cur_player == player1:
            cur_player = player2
        else:
            cur_player = player1
    

class RandomPlayer():
    def move(self, board, square, token):
        moves = get_possible_moves(board, square)
        return random.choice(moves)

class AggressivePlayer():
    def move(self, board, square, token):
        moves = get_possible_moves(board, square)
        possible_scores = []
        for move in moves:
            temp_board = board.copy()
            new_board = make_move(temp_board, move, token)[0]
            possible_scores.append((score(new_board), move))
        if token == "x":
            return max(possible_scores)[1]
        elif token == "o":
            return min(possible_scores)[1]
        else:
            print("Error: Token passed into AggressivePlayer move() method is not x or o.")

class BestPlayer():
    def __init__(self, d):
        self.depth = d
    def move(self, board, square, token):
        if token == "x":
            return max_move(board, square, self.depth, -100000000, 100000000)[1]
        elif token == "o":
            return min_move(board, square, self.depth, -100000000, 100000000)[1]
        else:
            print("Error: Token passed into BestPlayer move() method is not x or o.")

class User():
    def move(self, board, square, token):
        moves = get_possible_moves(board, square)
        print("Here are the possible moves you can play: " + str(moves))
        print("0 1 2\n3 4 5\n6 7 8")
        sub_board = input("Please print the index of the subboard in which you would like to play: ")
        index = input("Please print the index of the square on subboard " + sub_board + " in which you would like to play: ")
        return((int(sub_board), int(index)))
            
players = {
    "RANDOM" : RandomPlayer(),
    "BEST" : BestPlayer(6),
    "USER" : User(),
    "AGGRESSIVE" : AggressivePlayer()
}

play_game(players[sys.argv[1]], players[sys.argv[2]])
