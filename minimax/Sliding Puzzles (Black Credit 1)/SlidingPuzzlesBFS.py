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

def find_solution_BiBFS(board):
    reached_from_initial = {board}
    goal = find_goal(board)
    reached_from_goal = {goal}
    queue_initial = deque([(board, )])
    queue_goal = deque([(goal, )])

    while len(queue_initial) != 0 and len(queue_goal) != 0:
        # processing queue_initial
        size_initial = len(queue_initial)
        for i in range(0, size_initial):
            state1 = queue_initial.popleft()
            children = get_children(state1[0])
            for child in children:
                if child in reached_from_goal:
                    while len(queue_goal) != 0:
                        path = queue_goal.popleft()
                        if path[0] == child:
                            return state1[::-1] + path
                elif child not in reached_from_initial:
                    queue_initial.append((child, ) + state1)
                    reached_from_initial.add(child)
        
        # processing queue_goal
        size_goal = len(queue_goal)
        for i in range(0, size_goal):
            state2 = queue_goal.popleft()
            children = get_children(state2[0])
            for child in children:
                if child in reached_from_initial:
                    while len(queue_initial) != 0:
                        path = queue_initial.popleft()
                        if path[0] == child:
                            return path[::-1] + state2
                elif child not in reached_from_goal:
                    queue_goal.append((child, ) + state2)
                    reached_from_goal.add(child)

    return None


# Printing puzzles and their goal states
file_name = sys.argv[1]
with open(file_name) as f:
    line_list = [line.strip() for line in f]
    i = 0
    for line in line_list:
        size = 4
        board = line.strip()
        start = time.perf_counter()
        tup = find_solution(board)
        end = time.perf_counter()
        num_of_moves = len(tup) - 1
        print("Run with BFS: Line %s: %s, %s moves found in %s seconds" % (i, board, num_of_moves, end - start))
        start2 = time.perf_counter()
        tup2 = find_solution_BiBFS(board)
        end2 = time.perf_counter()
        num_of_moves_2 = len(tup2) - 1
        print("Run with BiBFS: Line %s: %s, %s moves found in %s seconds" % (i, board, num_of_moves_2, end2 - start2))
        i += 1
