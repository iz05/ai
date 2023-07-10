# Isabella Zhu
# AI Period 2

# THIS PROGRAM ONLY WORKS FOR 4 x 4 PUZZLES THAT HAVE GOAL STATE ABCDEFGHIJKLMNO.

# VERSION 4: generating all possible 4 letter combos to (hopefully) speed up code

from collections import deque
from heapq import heappush, heappop, heapify
import sys
import time

# GLOBAL VARIABLES

# TILE_LOCATIONS = {
#     "A" : (0, 0),
#     "B" : (0, 1),
#     "C" : (0, 2),
#     "D" : (0, 3),
#     "E" : (1, 0),
#     "F" : (1, 1),
#     "G" : (1, 2),
#     "H" : (1, 3),
#     "I" : (2, 0),
#     "J" : (2, 1),
#     "K" : (2, 2),
#     "L" : (2, 3),
#     "M" : (3, 0),
#     "N" : (3, 1),
#     "O" : (3, 2)
# }

TILE_LOCATIONS = {
    "A" : (0, 1),
    "B" : (0, 2),
    "C" : (0, 3),
    "D" : (1, 0),
    "E" : (1, 1),
    "F" : (1, 2),
    "G" : (1, 3),
    "H" : (2, 0),
    "I" : (2, 1),
    "J" : (2, 2),
    "K" : (2, 3),
    "L" : (3, 0),
    "M" : (3, 1),
    "N" : (3, 2),
    "O" : (3, 3)
}

LINEAR_CONFLICTS = {
    "" : 0,
    "<" : 0, # 01
    ">" : 1, # 10
    "<<<" : 0, # 012
    "<<>" : 1, # 021
    "><<" : 1, # 102
    "<>>" : 1, # 120
    ">><" : 1, # 201
    ">>>" : 2, # 210
    "<<<<<<" : 0, # 0123
    "<<<<<>" : 1, # 0132
    "<<<><<" : 1, # 0213
    "<<<<>>" : 1, # 0231
    "<<<>><" : 1, # 0312
    "<<<>>>" : 2, # 0321
    "><<<<<" : 1, # 1023
    "><<<<>" : 2, # 1032
    "<><><<" : 1, # 1203
    "<<><>>" : 1, # 1230
    "<><>><" : 2, # 1302
    "<<>>>>" : 2, # 1320
    ">><<<<" : 1, # 2013
    "><><<>" : 2, # 2031
    ">><><<" : 2, # 2103
    "><><>>" : 2, # 2130 
    "<>>>><" : 2, # 2301
    "<>>>>>" : 2, # 2310
    ">>><<<" : 1, # 3012
    ">>><<>" : 2, # 3021
    ">>>><<" : 2, # 3102
    ">>><>>" : 2, # 3120
    ">>>>><" : 2, # 3201
    ">>>>>>" : 3 # 3210
}

# GOAL = "ABCDEFGHIJKLMNO."
GOAL = ".ABCDEFGHIJKLMNO"

SIZE = 4

FOUR_LETTER_COMBOS = {}

def generate_combos():
    letters = set()
    for i in range(0, len(GOAL)):
        letters.add(GOAL[i])
    for i in range(0, SIZE):
        for l1 in letters:
            for l2 in letters - {l1}:
                for l3 in letters - {l1, l2}:
                    for l4 in letters - {l1, l2, l3}:
                        string = l1 + l2 + l3 + l4
                        FOUR_LETTER_COMBOS[(i, "r", string)] = 2 * conflict(helper_row_2(i, string)) # r = row
    for i in range(0, SIZE):
        for l1 in letters:
            for l2 in letters - {l1}:
                for l3 in letters - {l1, l2}:
                    for l4 in letters - {l1, l2, l3}:
                        string = l1 + l2 + l3 + l4
                        FOUR_LETTER_COMBOS[(i, "c", string)] = 2 * conflict(helper_col_2(i, string)) # c = column


def print_puzzle(size, board):
    i = 0
    row = ""
    while(i < len(board)):
        row += board[i] + " "
        i += 1
        if(i % size == 0):
            print(row)
            row = ""

def conflict(row): # row is a string of x numbers, x <= 4
    code_string = ""
    for i in range(0, len(row) - 1):
        for j in range(i + 1, len(row)):
            if row[i] > row[j]:
                code_string += ">"
            else:
                code_string += "<"
    return LINEAR_CONFLICTS[code_string]

def helper_row_2(i, row):
    r = ""
    for col in range(0, SIZE):
        letter = row[col]
        if letter != ".":
            actual_row, actual_col = TILE_LOCATIONS[letter]
            if i == actual_row:
                r += letter
    return r

def helper_col_2(i, col):
    c = ""
    for row in range(0, SIZE):
        letter = col[i]
        if letter != ".":
            actual_row, actual_col = TILE_LOCATIONS[letter]
            if i == actual_col:
                c += letter
    return c

def helper_row(i, board):
    r = ""
    for j in range(0, SIZE):
        r += board[i * SIZE + j]
    return r

def helper_col(i, board):
    c = ""
    for j in range(0, SIZE):
        c += board[j * SIZE + i]
    return c

def conflict_heuristic(board):
    heuristic = 0
    # do the rows first
    for row in range(0, SIZE):
        heuristic += FOUR_LETTER_COMBOS[(row, "r", helper_row(row, board))]
    # columns next
    for col in range(0, SIZE):
        heuristic += FOUR_LETTER_COMBOS[(col, "c", helper_col(col, board))]
    return heuristic

# returns [(child, +-1)], -1 means taxicab decreased, +1 means taxicab increased
def get_children(board):
    children = []
    size = int(len(board) ** 0.5)

    # a : row
    # b : column
    
    ind = board.index(".")
    a = ind // size
    b = ind % size

    # possible_states = [(a + c, b + d) for c in range(-1, 2) for d in range(-1, 2) if 0 <= a + c < size and 0 <= b + d < size and c * d == 0 and (c != 0 or d != 0)]

    # for c, d in possible_states:
    #     ind2 = c * size + d
    #     children.append(board[0 : min(ind, ind2)] + board[max(ind, ind2)] + board[min(ind, ind2) + 1 : max(ind, ind2)] + board[min(ind, ind2)] + board[max(ind, ind2) + 1 : ])


    # shifting left tile to the right
    if b > 0:
        net_change = 1
        ind2 = ind - 1
        tile = board[ind2]
        row, col = TILE_LOCATIONS[tile]
        if col > b - 1:
            net_change = -1
        child = board[0 : min(ind, ind2)] + board[max(ind, ind2)] + board[min(ind, ind2) + 1 : max(ind, ind2)] + board[min(ind, ind2)] + board[max(ind, ind2) + 1 : ]
        if col == b - 1 or col == b:
            net_change += FOUR_LETTER_COMBOS[(col, "c", helper_col(col, child))] - FOUR_LETTER_COMBOS[(col, "c", helper_col(col, board))]
        children.append((child, net_change))

    # shifting right tile to the left
    if b < size - 1:
        net_change = 1
        ind2 = ind + 1
        tile = board[ind2]
        row, col = TILE_LOCATIONS[tile]
        if col < b + 1:
            net_change = -1
        child = board[0 : min(ind, ind2)] + board[max(ind, ind2)] + board[min(ind, ind2) + 1 : max(ind, ind2)] + board[min(ind, ind2)] + board[max(ind, ind2) + 1 : ]
        if col == b + 1 or col == b:
            net_change += FOUR_LETTER_COMBOS[(col, "c", helper_col(col, child))] - FOUR_LETTER_COMBOS[(col, "c", helper_col(col, board))]
        children.append((child, net_change))

    # shifting bottom tile up
    if a < size - 1:
        net_change = 1
        ind2 = ind + size
        tile = board[ind2]
        row, col = TILE_LOCATIONS[tile]
        if row < a + 1:
            net_change = -1
        child = board[0 : min(ind, ind2)] + board[max(ind, ind2)] + board[min(ind, ind2) + 1 : max(ind, ind2)] + board[min(ind, ind2)] + board[max(ind, ind2) + 1 : ]
        if row == a + 1 or row == a:
            net_change += FOUR_LETTER_COMBOS[(row, "r", helper_row(row, child))] - FOUR_LETTER_COMBOS[(row, "r", helper_row(row, board))]
        children.append((child, net_change))

    # shifting upper tile down
    if a > 0:
        net_change = 1
        ind2 = ind - size
        tile = board[ind2]
        row, col = TILE_LOCATIONS[tile]
        if row > a - 1:
            net_change = -1
        child = board[0 : min(ind, ind2)] + board[max(ind, ind2)] + board[min(ind, ind2) + 1 : max(ind, ind2)] + board[min(ind, ind2)] + board[max(ind, ind2) + 1 : ]
        if row == a - 1 or row == a:
            net_change += FOUR_LETTER_COMBOS[(row, "r", helper_row(row, child))] - FOUR_LETTER_COMBOS[(row, "r", helper_row(row, board))]
        children.append((child, net_change))

    return children

def parity_check(size, board):
    arr = []
    index = -1
    for i in range(0, len(board)):
        if board[i] != ".":
            arr.append(board[i])
        else:
            index = i
    count = 0
    for i in range(0, len(board) - 2):
        for j in range(i + 1, len(board) - 1):
            if arr[i] > arr[j]:
                count += 1
    row_num = index // size          
    if size % 2 == 0:
        return (count - row_num + 1) % 2 == 0
    else:
        return count % 2 == 0

def test_parity_check(filename):
    with open(filename) as f:
        line_list = [line.strip() for line in f]
        for line in line_list:
            size = int(line[0])
            board = line[1:].strip()
            print("Board is solvable? " + str(parity_check(size, board)))

def taxicab(size, board):
    s = 0
    goal = GOAL
    for i in range(0, len(board)):
        if board[i] != ".":
            num = goal.index(board[i])
            row1 = num // size
            col1 = num % size
            row2 = i // size
            col2 = i % size
            s += abs(col1 - col2) + abs(row1 - row2)
    return s

def a_star(size, board):
    # if not parity_check(size, board):
    #     return None
    closed = set()
    fringe = []
    # store in form (heuristic, depth, board)
    heappush(fringe, (taxicab(size, board) + conflict_heuristic(board), 0, board)) 
    while len(fringe) != 0:
        state = heappop(fringe)
        if state[2] == GOAL:
            return state[1] # returns the number of moves taken
        if state[2] not in closed:
            closed.add(state[2])
            for child, num in get_children(state[2]):
                if child not in closed:
                    tup = (
                        state[0] + 1 + num,
                        state[1] + 1, # 1 extra move was taken
                        child
                    )
                    heappush(fringe, tup)
    return None

generate_combos()
print("Finished generating all possible combinations for rows and columns.")
with open("korf100_37.txt") as f:
    i = 37
    total_start = time.perf_counter()
    for line in [line.strip() for line in f]:
        start = time.perf_counter()
        length = a_star(SIZE, line)
        end = time.perf_counter()
        print("Line %s: %s, A* - %s moves found in %s seconds" % (i, line, length, end - start))
        i += 1
    total_end = time.perf_counter()
    print("All puzzles were solved in %s seconds." % (total_end - total_start))
