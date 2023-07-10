from collections import deque
import sys
import time

# Global Variables
SIZE = 6

# Input pieces here, X is the car that should escape
start_pieces = {
    "X" : ("h", 2, (2, 1)),
    "A" : ("v", 2, (0, 0)),
    "B" : ("v", 2, (0, 1)),
    "C" : ("h", 3, (0, 2)),
    "D" : ("v", 2, (0, 5)),
    "E" : ("v", 3, (1, 4)),
    "F" : ("v", 2, (2, 5)),
    "G" : ("v", 2, (2, 0)),
    "H" : ("h", 2, (3, 1)),
    "I" : ("v", 2, (4, 2)),
    "J" : ("h", 2, (5, 0)),
    "K" : ("h", 2, (5, 3)),
}

def get_positions(pieces):
    positions = []
    for i in range(0, SIZE):
        l = []
        for j in range(0, SIZE):
            l.append(".")
        positions.append(l)

    # Update positions based on pieces
    for piece, tup in pieces.items():
        if tup[0] == "v": # if piece is vertical
            startX, startY = tup[2]
            size = tup[1]
            for i in range(0, size):
                positions[startX + i][startY] = piece
        else:
            startX, startY = tup[2]
            size = tup[1]
            for i in range(0, size):
                positions[startX][startY + i] = piece
    return positions

start_positions = get_positions(start_pieces)
start_board = (start_pieces, start_positions)

def print_board(positions):
    for i in range(0, SIZE):
        row = ""
        for j in range(0, SIZE):
            row += positions[i][j] + " "
        print(row)

def get_moves(piece, pieces, positions): # helper method for get_children
    orientation, length, position = pieces[piece]
    row, col = position
    moves = set() # given by a nonzero integer
    if orientation == "h":
        for c in range(col + 1, SIZE - length + 1):
            if positions[row][c + length - 1] != ".":
                break
            else:
                moves.add(c - col)
        for c in range(col - 1, -1, -1):
            if positions[row][c] != ".":
                break
            else:
                moves.add(c - col)
    else:
        for r in range(row + 1, SIZE - length + 1):
            if positions[r + length - 1][col] != ".":
                break
            else:
                moves.add(r - row)
        for r in range(row - 1, -1, -1):
            if positions[r][col] != ".":
                break
            else:
                moves.add(r - row)
    return moves


def get_children(board):
    pieces, positions = board
    children = []
    for piece, tup in pieces.items():
        moves = get_moves(piece, pieces, positions)
        for move in moves:
            child_pieces = pieces.copy()
            if tup[0] == "v":
                child_pieces[piece] = (tup[0], tup[1], (tup[2][0] + move, tup[2][1]))
            else:
                child_pieces[piece] = (tup[0], tup[1], (tup[2][0], tup[2][1] + move))
            child_positions = get_positions(child_pieces)
            children.append((child_pieces, child_positions))
        if piece == "X":
            if (SIZE - 2 - tup[2][1]) in moves: # Goal state is achievable
                child_pieces = pieces.copy()
                del child_pieces["X"]
                child_positions = get_positions(child_pieces)
                children.append((child_pieces, child_positions))
    return children

def goal_test(board):
    pieces = board[0]
    if "X" not in pieces:
        return True
    return False

def BFS():
    visited = [start_board[1]]
    queue = deque([(start_board, )])
    while len(queue) != 0:
        tup = queue.popleft()
        board = tup[0]
        if goal_test(board):
            return tup
        else:
            for child in get_children(board):
                if child[1] not in visited:
                    visited.append(child[1])
                    queue.append((child, ) + tup)
    return None

def output(tup):
    tup2 = tup[::-1]
    for tup3 in tup2:
        print_board(tup3[1])
        print()

# Testing
# for child in get_children(start_board):
#     print_board(child[1])
#     print()
# print_board(start_positions)
# print()
tup = BFS()
output(tup)
print("This puzzle took %s moves." % (len(tup) - 1))