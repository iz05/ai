# Isabella Zhu
# 09/30/21
# Calibron

# You are given code to read in a puzzle from the command line.  The puzzle should be a single input argument IN QUOTES.
# A puzzle looks like this: "56 56 28x14 32x11 32x10 21x18 21x18 21x14 21x14 17x14 28x7 28x6 10x7 14x4"
# The code below breaks it down:
# puzzle_height is the height (number of rows) of the puzzle
# puzzle_width is the width (number of columns) of the puzzle
# rectangles is a list of tuples of rectangle dimensions



# INSTRUCTIONS:
#
# First check to see if the sum of the areas of the little rectangles equals the big area.
# If not, output precisely this - "Containing rectangle incorrectly sized."
#
# Then try to solve the puzzle.
# If the puzzle is unsolvable, output precisely this - "No solution."
#
# If the puzzle is solved, output ONE line for EACH rectangle in the following format:
# row column height width
# where "row" and "column" refer to the rectangle's top left corner.
#
# For example, a line that says:
# 3 4 2 1
# would be a rectangle whose top left corner is in row 3, column 4, with a height of 2 and a width of 1.
# Note that this is NOT the same as 3 4 1 2 would be.  The orientation of the rectangle is important.
#
# Your code should output exactly one line (one print statement) per rectangle and NOTHING ELSE.
# If you don't follow this convention exactly, my grader will fail.

# import statements
from heapq import heappush, heappop
import sys
import time

# states are stored as ( heap(edges), list of pieces, dimX, dimY, list of pieces already placed )
# edge = (y, x1, x2)

def get_edge(state):
    edges = state[0]

    edge = heappop(edges)
    if len(edges) != 0:
        next_edge = min(edges)

        while(next_edge is not None and next_edge[0] == edge[0] and (next_edge[1] == edge[2] + 1 or edge[1] == next_edge[2] + 1)): # if edges are same level and can be merged
            next_edge = heappop(edges)
            edge = (edge[0], min(edge[1], next_edge[1]), max(edge[2], next_edge[2]))
            next_edge = None
            if len(edges) != 0:
                next_edge = min(edges)
    
    return edge

def place_piece(state, piece):
    edges, pieces, dimX, dimY, sequence = state # unpacking tuple

    y, x1, x2 = get_edge(state) # returns uppermost then leftmost edge

    if y + piece[1] <= dimY and x1 + piece[0] - 1 <= x2: # check if piece can be oriented horizontally
        edge1 = (y + piece[1], x1, x1 + piece[0] - 1)
        heappush(edges, edge1)
        if x1 + piece[0] - 1 < x2:
            edge2 = (y, x1 + piece[0], x2)
            heappush(edges, edge2)
        sequence.append(str(y) + " " + str(x1) + " " + str(piece[1]) + " " + str(piece[0]))
        return True

    # elif y + piece[0] <= dimY and x1 + piece[1] - 1 <= x2: # check if piece can be oriented vertically
    #     edge1 = (y + piece[0], x1, x1 + piece[1] - 1)
    #     heappush(edges, edge1)
    #     if x1 + piece[1] - 1 < x2:
    #         edge2 = (y, x1 + piece[1], x2)
    #         heappush(edges, edge2)
    #     sequence.append(str(y) + " " + str(x1) + " " + str(piece[0]) + " " + str(piece[1]))
    #     return True

    return False # returns false if none of the orientations work

def backtrack(state):
    edges, pieces, dimX, dimY, sequence = state
    if len(pieces) == 0:
        return state
    for i in range(0, len(pieces)):
        piece = pieces[i]
        new_pieces_1 = pieces[ : i] + pieces[i + 1 : ]
        new_state_1 = (edges.copy(), new_pieces_1, dimX, dimY, sequence.copy())
        if place_piece(new_state_1, piece) == True: # piece can be placed
            final_state = backtrack(new_state_1)
            if final_state != None:
                return final_state
        flipped_piece = (piece[1], piece[0])
        new_pieces_2 = pieces[ : i] + pieces[i + 1 : ]
        new_state_2 = (edges.copy(), new_pieces_2, dimX, dimY, sequence.copy())
        if place_piece(new_state_2, flipped_piece) == True:
            final_state = backtrack(new_state_2)
            if final_state != None:
                return final_state
    return None

def solve():
    # states are stored as ( heap(edges), list of pieces, dimX, dimY, list of pieces already placed (called sequence) )
    edges = []
    sequence = []

    puzzle = sys.argv[1].split()
    dimY = int(puzzle[0])
    dimX = int(puzzle[1])
    pieces = [(int(temp.split("x")[0]), int(temp.split("x")[1])) for temp in puzzle[2:]]
    pieces.sort(key = lambda x : -1 * x[0] * x[1]) # sort by area, try placing tiles with max area first
    heappush(edges, (0, 0, dimX - 1))

    # check if rectangles are incorrectly sized
    pieces_sum = 0
    for piece in pieces:
        pieces_sum += piece[0] * piece[1]
    if pieces_sum != dimX * dimY:
        print("Containing rectangle incorrectly sized.")
        return

    state = (edges, pieces, dimX, dimY, sequence)
    solved_state = backtrack(state)

    if solved_state == None:
        print("No solution.")
        return

    for output in solved_state[4]:
        print(output)

solve()