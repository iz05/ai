# Isabella Zhu
# AI Period 2
from collections import deque
from heapq import heappush, heappop, heapify
import sys
import time

path_lengths = {}
multiple_paths = {}
no_center = {}
has_center = {}
for i in range(0, 32):
    path_lengths[i] = set()
    multiple_paths[i] = set()
    no_center[i] = set()
    has_center[i] = set()

GOAL = "12345678."

def center_blank(board):
    return board[4] == "."

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

def BFS_all_states():
    reached = {GOAL}
    queue = deque([(GOAL, 0)])
    while len(queue) != 0:
        board, num = queue.popleft()
        path_lengths[num].add(board)
        for child in get_children(board):
            if child not in reached:
                reached.add(child)
                queue.append((child, num + 1))

def BFS_all_states_v2():
    reached = {GOAL}
    queue = deque([(GOAL, 0)])
    size = 0
    while len(queue) != 0:
        temp_visited = set()
        while len(queue) != 0 and queue[0][1] == size:
            board, num = queue.popleft()
            if board in path_lengths[num]:
                multiple_paths[num].add(board)
            path_lengths[num].add(board)
            for child in get_children(board):
                if child not in reached:
                    temp_visited.add(child)
                    queue.append((child, num + 1))
        reached.update(temp_visited)     
        size += 1

def BFS_all_states_no_blank():
    reached = {GOAL}
    queue = deque([(GOAL, 0)])
    while len(queue) != 0:
        board, num = queue.popleft()
        no_center[num].add(board)
        for child in get_children(board):
            if child not in reached and not center_blank(child):
                reached.add(child)
                queue.append((child, num + 1))

def BFS_all_states_with_blank():
    reached = {GOAL}
    queue = deque([(GOAL, 0, False)])
    while len(queue) != 0:
        board, num, b = queue.popleft()
        if b:
            has_center[num].add(board)
        for child in get_children(board):
            if child not in reached:
                reached.add(child)
                if center_blank(child) or b:
                    queue.append((child, num + 1, True)) 
                else:
                    queue.append((child, num + 1, False))   

# exploration 1
BFS_all_states_v2()
print("Exploration #1: Path Lengths")
data = [["Min Sol Length", "# of States", "Unique", "Multiple"]]
for i in range(0, 32):
    temp_list = [str(i), str(len(path_lengths[i])), str(len(path_lengths[i]) - len(multiple_paths[i])), str(len(multiple_paths[i]))]
    data.append(temp_list)
col_width = max(len(word) for row in data for word in row) + 2  # padding
for row in data:
    print("".join(word.ljust(col_width) for word in row))
print()

# exploration 2
print("Exploration #2: Path Restraints")
BFS_all_states_no_blank()
BFS_all_states_with_blank()
total_no_blank = 0
total_with_blank = 0
output_data = [["Min Sol Length", "Has Blank", "No Blank"]]
for i in range(0, 32):
    temp = [str(i), str(len(has_center[i])), str(len(no_center[i]))]
    total_no_blank += len(no_center[i])
    total_with_blank += len(has_center[i])
    output_data.append(temp)
col_width = max(len(word) for row in output_data for word in row) + 2  # padding
for row in output_data:
    print("".join(word.ljust(col_width) for word in row))
print("At least one blank: " + str(total_with_blank))
print("No blanks: " + str(total_no_blank))