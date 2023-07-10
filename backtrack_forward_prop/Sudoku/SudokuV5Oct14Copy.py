# Isabella Zhu

import sys
from collections import deque
import time

# final version of Sudoku

N = 0
CHAR_STRING = ""
subblock_height = 0
subblock_width = 0
symbol_set = None
constraint_sets = [] # 3N sets of constraints, N for rows, N for columns, N for subgrids
constraints = {} # key = index of square, value = set of neighbors
constraint_sets_2 = {} # key = index of square, value = list of constraint sets that index is a part of

# board will be stored as a list of strings, each string stores all possibilities of characters

def sudoku(filename):
    count = 1
    with open(filename) as f:
        lines = [line.strip() for line in f]
        lines.sort(key = lambda x : len(x))
        for line in lines:
            solve(line)
            print("Puzzle %s solved" % count)
            count += 1

def check_puzzle(state):
    for symbol in symbol_set:
        if state.count(symbol) != N:
            print("PUZZLE IS WRONG")
            sys.exit()

def set_vars(state):
    global N, subblock_height, subblock_width, symbol_set, constraint_sets, constraints, CHAR_STRING
    constraint_sets = []
    constraints = {}

    N = int(len(state) ** 0.5)
    CHAR_STRING = ""

    for i in range(int(N ** 0.5), 0, -1):
        if N % i == 0:
            subblock_height = i
            break
    
    subblock_width = N // i

    symbol_set = set()
    numbers = [chr(i) for i in range(49, 58)]
    letters = [chr(i) for i in range(65, 91)]
    symbols = numbers + letters

    for i in range(0, N):
        symbol_set.add(symbols[i])
        CHAR_STRING += symbols[i]

    for i in range(0, N): 
        constraint_sets.append({N * i + j for j in range(0, N)}) # rows
        constraint_sets.append({N * j + i for j in range(0, N)}) # columns
    
    for w in range(0, N, subblock_width): # columns
        for h in range(0, N, subblock_height): # rows
            constraint_sets.append({N * (i + h) + (w + j) for i in range(0, subblock_height) for j in range(0, subblock_width)}) # blocks

    for i in range(0, N * N):
        constraints[i] = set()
        constraint_sets_2[i] = []
        for s in constraint_sets:
            if i in s:
                constraints[i].update(s)
                constraint_sets_2[i].append(s)
        constraints[i] = constraints[i] - {i}

def generate_state(line):
    state = []
    for i in range(0, len(line)):
        if line[i] != ".":
            state.append(line[i])
        else:
            state.append(CHAR_STRING[ : ])
    return state

def print_board(state):
    string = ""
    index = 0
    for i in range(0, N + subblock_width - 1):
        if i % (subblock_height + 1) == subblock_height:
            for j in range(0, N + subblock_height - 1):
                string += "--"
        else:
            for j in range(0, N + subblock_height - 1):
                if j % (subblock_width + 1) == subblock_width:
                    string += "| "
                else:
                    if len(state[index]) == 1:
                        string += state[index] + " "
                    else:
                        string += ". "
                    index += 1
        string += "\n"
    print(string)

def number_of_instances(state):
    for symbol in symbol_set:
        print("There are %s occurences of %s in this state." % (state.count(symbol), symbol))

def get_next_variable(state):
    smallest_length = N + 1
    var = -1
    for i in range(0, N * N):
        if len(state[i]) != 1 and len(state[i]) < smallest_length:
            var = i
            smallest_length = len(state[i])
    return var

def get_sorted_values(index, state):
    return state[index]

def forward_looking(new_state):
    change = False
    one_solution_indices = deque([])
    for i in range(0, len(new_state)):
        if len(new_state[i]) == 1:
            one_solution_indices.append(i)
    
    while len(one_solution_indices) != 0:
        index = one_solution_indices.popleft()
        for neighbor in constraints[index]:
            if new_state[index] in new_state[neighbor]:
                change = True
                i = new_state[neighbor].find(new_state[index])
                new_state[neighbor] = new_state[neighbor][ : i] + new_state[neighbor][i + 1 :]
                if len(new_state[neighbor]) == 0:
                    return None
                elif len(new_state[neighbor]) == 1:
                    one_solution_indices.append(neighbor)
    
    if change == True:
        new_state = constraint_propagation(new_state)
    return new_state

def constraint_propagation(new_state):
    change = False
    for set in constraint_sets:
        for value in CHAR_STRING:
            count = 0
            index = -1
            for item in set:
                if value in new_state[item]:
                    count += 1
                    index = item
            if count == 0:
                return None
            elif count == 1:
                new_state[index] = value
                change = True
    if change == True:
        new_state = forward_looking(new_state)
    return new_state

def place(state, index, value):
    # inefficient code
    # remove values
    # while len(state[index]) > 1:
    #     char = state[index][0]
    #     if char != value:
    #         state[index] = state[index][1 : ]
    #     else:
    #         state[index] = state[index][0] + state[index][2 : ]
    #     state = remove(state, index, char)
    #     if state is None:
    #         return state


    ind = state[index].find(value)
    remove_values = state[index][0 : ind] + state[index][ind + 1 : ]
    state[index] = value
    for char in remove_values:
        state = remove(state, index, char) # removes values one by one
        if state is None:
            return state
    
    # forward looking on constraint sets
    for neighbor in constraints[index]:
        if value in state[neighbor]:
            remove_item(state, neighbor, value)
            if len(state[neighbor]) == 0:
                return None
            state = remove(state, neighbor, value)
            if state is None:
                return None
    
    return state

def remove(state, index, value):
    # check constraint propagation for three constraint sets
    for set in constraint_sets_2[index]:
        count = 0 # number of times that value appears in the set
        ind = -1
        for item in set:
            if value in state[item]:
                count += 1
                ind = item
        if count == 0:
            return None
        elif count == 1:
            if len(state[ind]) != 1:
                state = place(state, ind, value)
            if state is None:
                return None

    # check if there are n squares with the exact same n values    
    n = len(state[index])
    for set in constraint_sets_2[index]:
        indices = []
        for item in set:
            if len(state[item]) == n and state[item] == state[index]:
                indices.append(item)
        if len(indices) > n:
            return None
        elif len(indices) == n:
            remove_vals = [state[index][i] for i in range(0, n)]
            for item in set:
                if item not in indices:
                    for val in remove_vals:
                        if remove_item(state, item, val):
                            state = remove(state, item, val)
                            if state is None:
                                return None
    

    # check if there are two values that only occur in two squares
    # for set in constraint_sets_2[index]:
    #     for val1 in symbol_set:
    #         if val1 != value:
    #             indices = []

    #             should_break = False
    #             for item in set:
    #                 if val1 in state[item] and value in state[item]:
    #                     indices.append(item)
    #                 elif val1 in state[item] or value in state[item]:
    #                     should_break = True
    #                     break

    #             if should_break:
    #                 break

    #             if len(indices) == 2:
    #                 while len(state[indices[0]]) > 2:
    #                     ind = 0
    #                     char = state[indices[0]][0]
    #                     while char == val1 or char == value:
    #                         ind += 1
    #                         char = state[indices[0]][ind]
    #                     state[indices[0]] = state[indices[0]][0 : ind] + state[indices[0]][ind + 1 : ]
    #                     state = remove(state, indices[0], char)
    #                     if state is None:
    #                         return None
                        
    #                 while len(state[indices[1]]) > 2:
    #                     ind = 0
    #                     char = state[indices[1]][0]
    #                     while char == val1 or char == value:
    #                         ind += 1
    #                         char = state[indices[1]][ind]
    #                     state[indices[1]] = state[indices[1]][0 : ind] + state[indices[1]][ind + 1 : ]
    #                     state = remove(state, indices[1], char)
    #                     if state is None:
    #                         return None

    #             elif len(indices) == 1:
    #                 return None
    
    return state

def remove_item(state, index, val):
    if val in state[index]:
        ind = state[index].index(val)
        state[index] = state[index][:ind] + state[index][ind + 1:]
        return True
    return False

def backtrack(state):
    index = get_next_variable(state)
    if index == -1:
        return state
    if state is None:
        return None
    for value in get_sorted_values(index, state):
        new_state = state.copy()
        new_state = place(new_state, index, value)
        if new_state is not None:
            result = backtrack(new_state)
            if result is not None:
                return result
    return None

def print_line(state): # takes a list of strings and prints it
    output = ""
    for item in state:
        output += item
    print(output)

def solve(line):
    set_vars(line)
    state = generate_state(line)
    # print_board(state)
    state = forward_looking(state)
    # print_board(state)
    fin_state = backtrack(state)
    print_line(fin_state)
    # print_board(fin_state)
    check_puzzle(fin_state)
    # number_of_instances(fin_state)

start = time.perf_counter()
filename = sys.argv[1]
sudoku(filename)
end = time.perf_counter()
print("Puzzles solved in %s seconds." % (end - start))

# get a wrong result here
# solve(".7..23....2....1.147.......81......68.......326.6....8....53..1.")
# solution: 1785234636245781214765385368142742368175857132646412785378534612