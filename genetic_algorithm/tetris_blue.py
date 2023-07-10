import sys

HEIGHT = 20
WIDTH = 10

TETRIS_PIECES = {
    ("I", 0) : ["####", ],
    ("I", 1) : ["#", "#", "#", "#"],
    ("O", 0) : ["##", "##"],
    ("T", 0) : [" # ", "###"],
    ("T", 1) : ["# ", "##", "# "],
    ("T", 2) : ["###", " # "],
    ("T", 3) : [" #", "##", " #"],
    ("S", 0) : [" ##", "## "],
    ("S", 1) : ["# ", "##", " #"],
    ("Z", 0) : ["## ", " ##"],
    ("Z", 1) : [" #", "##", "# "],
    ("J", 0) : ["#  ", "###"],
    ("J", 1) : ["##", "# ", "# "],
    ("J", 2) : ["###", "  #"],
    ("J", 3) : [" #", " #", "##"],
    ("L", 0) : ["  #", "###"],
    ("L", 1) : ["# ", "# ", "##"],
    ("L", 2) : ["###", "#  "],
    ("L", 3) : ["##", " #", " #"],
}

def print_board(board):
    for row in board:
        print(row)

def convert_to_board(string):
    board = []
    for i in range(0, len(string), WIDTH):
        board.append(string[i : i + WIDTH])
    return board

def convert_to_string(board):
    string = ""
    for row in board:
        string += row
    return string

def get_largest_blank(board, col):
    space = -1
    for i in range(0, HEIGHT):
        if board[i][col] == " ":
            space = i
        else:
            return space
    return space

def width(piece):
    return len(TETRIS_PIECES[piece][0])

def height(piece):
    return len(TETRIS_PIECES[piece])

def get_height(piece, col):
    for i in range(height(piece) - 1, -1, -1):
        if TETRIS_PIECES[piece][i][col] == "#":
            return i
    return 0

def place_piece(board, piece, y, x):
    for b in range(0, height(piece)):
        for a in range(0, width(piece)):
            if TETRIS_PIECES[piece][b][a] == "#":
                board[y + b] = board[y + b][ : x + a] + "#" + board[y + b][x + a + 1 : ]

def remove_full_rows(board):
    remove_rows = []
    for i in range(0, HEIGHT):
        if board[i] == "#" * WIDTH:
            remove_rows.append(i)
    new_board = [" " * WIDTH, ] * len(remove_rows)
    for i in range(0, HEIGHT):
        if i not in remove_rows:
            new_board += [board[i], ]
    return (new_board, len(remove_rows))

def place_and_update(board, piece, col):
    min_y = HEIGHT
    for i in range(col, col + width(piece)):
        min_y = min(get_largest_blank(board, i) - get_height(piece, i - col), min_y)
    if min_y < 0:
        return None
    place_piece(board, piece, min_y, col)
    board, num_of_rows = remove_full_rows(board)
    return board

def part1():
    string = sys.argv[1]
    board = convert_to_board(string)
    f = open("tetrisout.txt", "w")
    for piece in TETRIS_PIECES:
        for col in range(0, WIDTH - width(piece) + 1):
            b = place_and_update(board.copy(), piece, col)
            if b == None:
                f.write("GAME OVER")
            else:
                b = convert_to_string(b)
                f.write(b)
            f.write("\n")
    f.close()

part1()