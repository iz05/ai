# Isabella Zhu
# AI Period 2
from collections import deque
from heapq import heappush, heappop, heapify
import sys
import time

def print_puzzle(size, board):
    i = 0
    row = ""
    while(i < len(board)):
        row += board[i] + " "
        i += 1
        if(i % size == 0):
            print(row)
            row = ""

def find_goal(board):
    temp = board.replace(".", "")
    temp = "".join(sorted(temp))
    return temp + "."

# returns a list of strings representing reachable states from a certain board
def get_children(board):
    children = []
    size = int(len(board) ** 0.5)

    # a : row
    # b : column
    
    ind = board.index(".")
    a = ind // size
    b = ind % size

    possible_states = [(a + c, b + d) for c in range(-1, 2) for d in range(-1, 2) if 0 <= a + c < size and 0 <= b + d < size and c * d == 0 and (c != 0 or d != 0)]

    for c, d in possible_states:
        ind2 = c * size + d
        children.append(board[0 : min(ind, ind2)] + board[max(ind, ind2)] + board[min(ind, ind2) + 1 : max(ind, ind2)] + board[min(ind, ind2)] + board[max(ind, ind2) + 1 : ])

    return children

def goal_test(board):
    return board == find_goal(board)

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

def BFS(size, board):
    if not parity_check(size, board):
        return None
    reached = {board}
    goal = find_goal(board)
    queue = deque([(board, )])
    while len(queue) != 0:
        state = queue.popleft()
        # state = queue.pop() # changes to DFS, not BFS
        if state[0] == goal:
            return state
        else:
            children = get_children(state[0])
            # children = get_children(state)
            for child in children:
                if child not in reached:
                    queue.append((child, ) + state)
                    reached.add(child)
    return None

def k_DFS(board, k):
    # how to store data: ((solution in tuple form), set of ancestors) 
    # to access the current board state -> tup[0][0]
    # to access the solution -> tup[0]
    # to access list of ancestors -> tup[1]
    fringe = [((board, ), set())]
    while len(fringe) != 0:
        state = fringe.pop()
        if goal_test(state[0][0]):
            return state[0][::-1]
        if len(state[0]) - 1 < k:
            for child in get_children(state[0][0]):
                if child not in state[1]:
                    temp_sol = (child, ) + state[0]
                    temp_ancestors = state[1].copy()
                    temp_ancestors.add(state[0][0])
                    fringe.append((temp_sol, temp_ancestors))
    return None

def ID_DFS(size, board):
    if not parity_check(size, board):
        return None
    max_depth = 0
    result = None
    while result is None:
        result = k_DFS(board, max_depth)
        max_depth = max_depth + 1
    return result

def taxicab(size, board):
    s = 0
    goal = find_goal(board)
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
    if not parity_check(size, board):
        return None
    closed = set()
    fringe = []
    heappush(fringe, (taxicab(size, board), (board, ))) 
    while len(fringe) != 0:
        state = heappop(fringe)
        if goal_test(state[1][0]):
            return state[1]
        if state[1][0] not in closed:
            closed.add(state[1][0])
            for child in get_children(state[1][0]):
                if child not in closed:
                    tup = (
                        taxicab(size, child) + len(state[1]),
                        (child, ) + state[1]
                    )
                    heappush(fringe, tup)
    return None

# file_name = sys.argv[1]
# with open(file_name) as f:
#     line_list = [line.strip() for line in f]
#     i = 0
#     for l in line_list:
#         line = l.split()
#         size = int(line[0])
#         board = line[1].strip()
#         char = line[2]

#         no_sol = False 

#         if char == "B" or char == "!":
#             start = time.perf_counter()
#             tup = BFS(size, board)
#             end = time.perf_counter()
#             if tup == None:
#                 print("Line %s: %s, no solution determined in %s seconds" % (i, board, end - start))
#                 no_sol = True
#             else:
#                 num_of_moves = len(tup) - 1
#                 print("Line %s: %s, BFS - %s moves found in %s seconds" % (i, board, num_of_moves, end - start))
        
#         if (char == "I" or char == "!") and not no_sol:
#             start = time.perf_counter()
#             tup = ID_DFS(size, board)
#             end = time.perf_counter()
#             if tup == None:
#                 print("Line %s: %s, no solution determined in %s seconds" % (i, board, end - start))
#                 no_sol = True
#             else:
#                 num_of_moves = len(tup) - 1
#                 print("Line %s: %s, ID-DFS - %s moves found in %s seconds" % (i, board, num_of_moves, end - start))
        
#         if (char == "A" or char == "!") and not no_sol:
#             start = time.perf_counter()
#             tup = a_star(size, board)
#             end = time.perf_counter()
#             if tup == None:
#                 print("Line %s: %s, no solution determined in %s seconds" % (i, board, end - start))
#                 no_sol = True
#             else:
#                 num_of_moves = len(tup) - 1
#                 print("Line %s: %s, A* - %s moves found in %s seconds" % (i, board, num_of_moves, end - start))

#         print()
#         i += 1
tup = a_star(4, "IABDNECJ.FKHMOGL")
print(tup)
print(str(len(tup) - 1))