from collections import deque 
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

# BFS Algorithm for generating all reachable outcomes
def how_many_reachable(n):
    board = "".join([str(i) for i in range(1, n * n)]) + "."
    print(board)
    reachable = {find_goal(board)}
    queue = deque([find_goal(board)])
    while len(queue) != 0:
        state = queue.popleft()
        children = get_children(state)
        for child in children:
            if child not in reachable:
                queue.append(child)
                reachable.add(child)
    return len(reachable)

def find_solution(board):
    reached = {board}
    goal = find_goal(board)
    queue = deque([(board, )])
    while len(queue) != 0:
        state = queue.popleft()
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

# longest solution path
def longest_solution(size):
    # how to keep track of data in queue: (board, parent_state)
    goal = "".join([str(i) for i in range(1, size * size)]) + "."
    reached = {goal}
    queue = deque([(goal, )])
    max_length = 0
    max_path = (goal, )
    while len(queue) != 0:
        state = queue.popleft()
        children = get_children(state[0])
        for child in children:
            if child not in reached:
                tup = (child, ) + state
                if len(tup) > max_length:
                    max_length = len(tup)
                    max_path = tup
                queue.append((child, ) + state)
                reached.add(child)
    return max_path

# sol = find_solution("1234567.8")[::-1]
# sol = find_solution(".53482176")[::-1]
# print(sol)
# print("Minimum number of moves to solve: %s" % (len(sol) - 1))

# Printing puzzles and their goal states
file_name = sys.argv[1]
with open(file_name) as f:
    line_list = [line.strip() for line in f]
    i = 0
    for line in line_list:
        size = int(line[0])
        board = line[1:].strip()
        start = time.perf_counter()
        tup = find_solution(board)
        end = time.perf_counter()
        num_of_moves = len(tup) - 1
        print("Line %s: %s, %s moves found in %s seconds" % (i, board, num_of_moves, end - start))
        i += 1

