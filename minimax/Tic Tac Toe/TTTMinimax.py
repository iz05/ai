# Tic Tac Toe - Minimax Algorithm
# Isabella Zhu
# 10/21/21

from collections import deque
import sys

def next_moves(board): # returns 1 is X wins, -1 if O wins, 0 if tie, and list of possible moves + who's turn it is to move otherwise
    x_count = board.count("X")
    o_count = board.count("O")

    win_char = "X"
    next_turn = "O"
    ret_num = 1

    if x_count == o_count:
        win_char = "O"
        next_turn = "X"
        ret_num = -1

    # check for wins
    for i in range(0, 3):
        if board[3 * i] == win_char and board[3 * i + 1] == win_char and board[3 * i + 2] == win_char: # check rows
            return ret_num
        elif board[i] == win_char and board[i + 3] == win_char and board[i + 6] == win_char: # check columns
            return ret_num
    
    if board[0] == win_char and board[4] == win_char and board[8] == win_char or board[2] == win_char and board[4] == win_char and board[6] == win_char: # check diagonals
        return ret_num
    
    # check for tie
    if board.count(".") == 0:
        return 0
    
    possible_moves = []
    possible_boards = []
    for i in range(0, len(board)):
        if board[i] == ".":
            possible_moves.append(i)
            possible_boards.append(board[0 : i] + next_turn + board[i + 1 : ])
    
    return (possible_moves, possible_boards, next_turn)

def find_all_games():
    start = "........."
    final_boards = set()
    finished_games = []
    games = deque([])
    games.append((start, ))

    while len(games) != 0:
        game = games.popleft()
        board = game[0]
        data = next_moves(board)
        if type(data) == int:
            finished_games.append((game, data))
            final_boards.add((board, data))
        else:
            moves, boards, char = data
            for index in moves:
                new_board = board[0 : index] + char + board[index + 1 : ]
                new_game = (new_board, ) + game
                games.append(new_game)
    
    print("There are %s possible games to be played." % len(finished_games)) # answer: 255168
    print("There are %s final board states." % len(final_boards)) # answer: 958

    counts = [0, 0, 0, 0, 0, 0] # X in 5, O in 6, X in 7, O in 8, X in 9, Draw

    for board_tuple in final_boards:
        board, state = board_tuple
        if state == 0: # tie
            counts[5] += 1
        elif state == 1:
            counts[board.count("X") * 2 - 6] += 1
        elif state == -1:
            counts[board.count("O") * 2 - 5] += 1
        else:
            print("Error: variable state is not 1, 0, or -1")
    
    print("X in 5: %s boards" % counts[0])
    print("O in 6: %s boards" % counts[1])
    print("X in 7: %s boards" % counts[2])
    print("O in 8: %s boards" % counts[3])
    print("X in 9: %s boards" % counts[4])
    print("Draws: %s boards" % counts[5])

def max_step(board):
    data = next_moves(board)
    if type(data) == int:
        return data
    results = []
    for b in data[1]:
        results.append(min_step(b))
    return max(results)

def max_move(board):
    data = next_moves(board)
    if type(data) == int:
        print()
        return data
    results = []
    index = 0
    cur = 0
    for b in data[1]:
        val = min_step(b)

        # print statements
        s = "win"
        if val == 0:
            s = "tie"
        elif val == -1:
            s = "loss"
        print("Moving at %s results in a %s." % (data[0][cur], s))

        results.append(val)
        if val > results[index]:
            index = cur
        cur += 1

    return data[0][index]

def min_step(board):
    data = next_moves(board)
    if type(data) == int:
        return data
    results = []
    for b in data[1]:
        results.append(max_step(b))
    return min(results)

def min_move(board):
    data = next_moves(board)
    if type(data) == int:
        return data
    results = []
    index = 0
    cur = 0
    for b in data[1]:
        val = max_step(b)

        # print statements
        s = "win"
        if val == 0:
            s = "tie"
        elif val == 1:
            s = "loss"
        print("Moving at %s results in a %s." % (data[0][cur], s))

        results.append(val)
        if val < results[index]:
            index = cur
        cur += 1
    return data[0][index]

def print_board(board):
    print("Current board:")
    print(board[0 : 3] + "    012")
    print(board[3 : 6] + "    345")
    print(board[6 : 9] + "    678")
    print()

def play_game(board):
    computer_token = "."
    player_token = "."
    cur_turn = "computer"
    if board == ".........":
        computer_token = input("Should I be X or O? ")
        print()
        if computer_token == "O":
            cur_turn = "player"
            player_token = "X"
        else:
            player_token = "O"
    else:
        if board.count("X") == board.count("O"):
            computer_token = "X"
            player_token = "O"
        else:
            computer_token = "O"
            player_token = "X"

    while(True):
        print_board(board)

        # check if anyone has won yet
        data = next_moves(board)

        if type(data) == int:
            if data == 1 and computer_token == "X" or data == -1 and computer_token == "O":
                print("I win!")
            elif data == 1 and computer_token == "O" or data == -1 and computer_token == "X":
                print("You win!")
            else:
                print("We tied!")
            break

        if cur_turn == "player": # player's turn
            indices = []
            for i in range(0, 9):
                if board[i] == ".":
                    indices.append(i)
            print("You can move to any of these spaces: " + str(indices)[1 : len(str(indices)) - 1] + ".")
            index = int(input("Your choice? "))
            print()
            board = board[0 : index] + player_token + board[index + 1 : ]
            cur_turn = "computer"

        else: # computer's turn
            index = -1
            if computer_token == "X":
                index = max_move(board)
            else:
                index = min_move(board)
            print()
            print("I choose space %s." % index)
            print()
            board = board[0 : index] + computer_token + board[index + 1 : ]
            cur_turn = "player"

play_game(sys.argv[1])
# find_all_games() 