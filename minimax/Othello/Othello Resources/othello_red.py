import sys
import math
def get_oppo(token):
    if token == "x":
        return "o"
    else:
        return "x"
def convert_64(a64board): #returns 100 board
    #takes a 64 board and adds a border of ?
    init = [a64board[i:i+8] for i in range(0, len(a64board), 8)]
    a100board = "??????????"
    for row in init:
        a100board= a100board + "?" + row + "?"
    a100board += "??????????"
    return a100board
def possible_moves(board, token): #returns list of 64index of available moves for token 
    #input a str 64board and ch token x or o
    #output list of possible square indexs token can be placed into
    #converts 64 to 100 board and then back to 64
    opponent = get_oppo(token)
    board = convert_64(board)
    spaces = []
    directions = [-11, -10, -9, -1, 1, 9, 10, 11] #nw, n, ne, w, e, sw, s, se
    opinds = [] #indexs of opponent token
    for ind, val in enumerate(board): #go thru board
        if val == opponent:#if value is opponent token
            opinds.append(ind) #add to opponent index list
    for i in opinds: #go through indexs of opponent
        for x in directions:#look at each direction
            x2=x #the x that iterates across teh entire direction line
            while board[i+x2:i+x2+1] == opponent:
                x2+= x
            if board[i+x2:i+x2+1] == token:#if the opposite direction has my token and the counter direction is empty/isnt a border
                if board[i-x:i-x+1] == ".":
                    spaces.append(i-x) #i add the counter direction index into indexs where i can go
    #convert space indexs back to 64 board form valid indexs
    for ind in spaces:
        board = board[:ind] + "S" + board[ind+1:] #1 is empty space
    board = board.replace('?', '')
    valid = [] #a list of indexes that are valid
    for int, i in enumerate(board):
        if i == "S":
            valid.append(int)
    return valid

def make_move(board, token, index):
    #input str 64board, ch token, int valid_move
    #ret 64board with placed token at index and flipped pieces
    board = board[:index] + "S" + board[index+1:] #places token
    board100 = convert_64(board) 
    index100 = board100.index("S") #uses S as a placeholder to find the right index in len100
    board100 = board100[:index100] + token + board100[index100+1:]
    directions = [-11, -10, -9, -1, 1, 9, 10, 11]
  #  print("100board", board100, "index100", index100)
    #check in which directions the token has same tokens matched and flip the opponent tokens in between
    for x in directions:
        board100 = flippy(board100, token, index100, x) #flips those spaces!!
    #convert back to 64
    board64 = board100.replace("?", "")
    return board64
def flippy(board, token, i, x): #x, 34, 10
    #inputs 100board, token, move index, direction)
    #returns the flipped board as a str
    opponent = get_oppo(token)
    x2=x #the x that iterates across teh entire direction line
    #print("initx2", x2)
    while board[i+x2:i+x2+1] == opponent: #finds the end of the trail thingy
       # print(board[i+x2:i+x2+1])
        
        x2 = x2 +x
     #   print("x2", x2)
    if board[i+x2:i+x2+1] == token:#if the end of the xooblah is xoox
        adding = i + x #index of next token
        while adding != i+x2: #goes down each index and makes it token
            board = board[:adding] + token + board[adding+1:]
            adding += x
    return board
corners_dict = {
    0: {1, 8, 9},
    7: {6, 14, 15},
    56: {57, 48, 49},
    63: {62, 54, 55}
}
edges_list = [2,3,4,5,6,16,23,24,31,32,39,40,47,58,59,60,61]
def scoring(board):
    global corners_dict, edges_list
    n = 0
    black = "x"
    white = "o"
    # if board.count(".") > 34:
    #     n = (len(possible_moves(board, black)) - len(possible_moves(board, white))) *2 #mobility
    # else:
    n = (len(possible_moves(board, black)) - len(possible_moves(board, white))) 
    # if board.count(".") <10:
    #     n+= board.count(black) - board.count(white) #just a greedy thing
    # black likes pos, white likes neg
    if board[:1] == black: #extra score for corner captured
        n+= 1000
    if board[7:8] == black:
        n+= 1000
    if board[63:] == black:
        n+= 1000
    if board[56:57] == black:
        n+= 1000
    if board[:1] == white:
        n-= 1000
    if board[7:8] == white:
        n-= 1000
    if board[63:] == white:
        n-= 1000
    if board[56:57] == white:
        n-= 1000
    #if corner blank:
    # for corner, adjs in corners_dict.items():
    #     if board[corner:corner+1] == ".": #having adjacent spaces to empty corners deducts points
    #         for adjacent in adjs:
    #             if board[adjacent:adjacent+1] == black:
    #                 n-=20
    #             elif board[adjacent:adjacent+1] == white:
    #                 n+=20
    #edges
    # for i in edges_list:
    #     if board[i:i+1] == "o":
    #         n-=10
    #     elif board[i:i+1] == "x":
    #         n+=10

    if "." not in board:    #if board filled, add/sub large amount to score
        if board.count("x") > board.count("o"): #x is black 
            n = 1000000 + ((board.count("x") - board.count("o"))) #change to differences
        elif board.count("x") < board.count("o"): #o wins, NOT a tie
            n = -1000000 - ((board.count("o") - board.count("x")))
    return n

def minimax(board, depth, alpha, beta, maxplayer): #black is max player
    if depth <= 0 or board.count(".") == 0:
        return scoring(board)
    
    if maxplayer:
        maxx = -math.inf
        possibles = possible_moves(board, "x") #x is maxer
        for move in possibles:
            new_board = make_move(board, "x", move)
            eval = minimax(new_board, depth-1, alpha, beta, False)
            maxx = max(maxx, eval) 
            alpha = max(alpha, eval) #"ALPHA/BETA PRUNING HERE" 
            if beta <= alpha:
                break
        return maxx
    else:
        minn = math.inf
        possibles = possible_moves(board, "o") #x is maxer
        for move in possibles:
            new_board = make_move(board, "o", move)
            eval = minimax(new_board, depth-1, alpha, beta, True)
            beta = min(beta, eval)#"ALPHA/BETA PRUNING HERE" 
            minn = min(minn, eval)
            if beta <= alpha:
                break
        return minn
def find_next_move(board, player, depth):
    #take the board state and see possible moves
    all_moves = possible_moves(board, player)
    best_move = all_moves[0]
    if player == "x":
        best_val = -math.inf
        for a_move in all_moves:
            x_board = make_move(board, player, a_move)
            move_val = minimax(x_board, depth, -math.inf, math.inf, True)
            if move_val > best_val:
                best_val = move_val
                best_move = a_move
    elif player == "o":
        best_val = math.inf
        for a_move in all_moves:
            o_board = make_move(board, player, a_move)
            move_val = minimax(o_board, depth, -math.inf, math.inf, False)
            if move_val < best_val:
                best_val = move_val
                best_move = a_move
    return best_move

# class Strategy():
#     def best_strategy(self, board, player, best_move, still_running):
#         depth = 1
#         for count in range(board.count(".")):  # No need to look more spaces into the future than exist at all
#             best_move.value = find_next_move(board, player, depth)
#             depth += 1

board = sys.argv[1] #python.exe othello2.py "...........................ox......oxx.....o...................." "x"
player = sys.argv[2]
depth = 1
for count in range(board.count(".")):  # No need to look more spaces into the future than exist at all
   print(find_next_move(board, player, depth))
   depth += 1