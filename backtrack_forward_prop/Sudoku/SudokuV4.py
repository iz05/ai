# Isabella Zhu

import sys
from collections import deque

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
    with open(filename) as f:
        lines = [line.strip() for line in f]
        for line in lines:
            solve(line)

def print_intermediate(state):
    output = ""
    for item in state:
        if len(item) > 1:
            output += "."
        else:
            output += item
    print(output)

def print_line(state): # takes a list of strings and prints it
    output = ""
    for item in state:
        output += item
    print(output)

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
                    string += state[index] + " "
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
    # new_state = state.copy()
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
                    # return None
                    new_state = None
                    return
                elif len(new_state[neighbor]) == 1:
                    one_solution_indices.append(neighbor)
    
    # if change == True:
    #     return constraint_propagation(new_state)

    # return new_state

def forward_looking_2(state, index, value):
    pass

def constraint_propagation(new_state):
    change = False

    # checks if exactly one square has a value in a constraint set
    for set in constraint_sets:
        for value in CHAR_STRING:
            count = 0
            index = -1
            for item in set:
                if value in new_state[item]:
                    count += 1
                    index = item
            if count == 0:
                new_state = None
                return
            elif count == 1:
                new_state[index] = value
                place(new_state, index, value)
                if new_state == None:
                    return
                change = True
    
    # checks if two squares have two values that only occur in those two squares
    # for set in constraint_sets:
    #     for value1 in CHAR_STRING:
    #         for value2 in CHAR_STRING:
    #             if value2 > value1:
    #                 indices = []
    #                 for item in set:
    #                     if value1 in new_state[item] and value2 in new_state[item]:
    #                         indices.append(item)
    #                 if len(indices) == 2:
    #                     for item in set:
    #                         if item not in indices:
    #                             # delete value1
    #                             ind1 = new_state[item].find(value1)
    #                             new_state[item] = new_state[item][ : ind1] + new_state[item][ind1 + 1 :]
    #                             # delete value2
    #                             ind2 = new_state[item].find(value2)
    #                             new_state[item] = new_state[item][ : ind2] + new_state[item][ind2 + 1 :]

    if change == True:
        forward_looking(new_state)

def place(state, index, val):
    i = state[index].find(val)
    if i == -1:
        state = None
        return
    state[index] = val
    for char in state[index][0 : i] + state[index][i + 1 : ]:
        remove(state, index, char)
        if state == None:
            return None
    # return new_state

def remove(new_state, index, val):
    for set in constraint_sets_2[index]:
        count = 0
        ind = -1
        for item in set:
            if val in new_state[item]:
                count += 1
                ind = item
        if count == 0:
            new_state = None
            return
        elif count == 1:
            if len(new_state[ind]) != 1:
                place(new_state, ind, val)
                if new_state == None:
                    return

# def backtrack(state):
#     index = get_next_variable(state)
#     if index == -1:
#         return state
#     for value in get_sorted_values(index, state):
#         new_state = state.copy()
#         new_state = place(new_state, index, value)
#         if new_state is not None:
#             result = backtrack(new_state)
#             if result is not None:
#                 return result
#     return None

def backtrack(state):
    index = get_next_variable(state)
    if index == -1:
        return state
    for value in get_sorted_values(index, state):
        new_state = state.copy()
        # place(state, index, value)
        new_state[index] = value
        forward_looking(new_state)
        if new_state is not None:
            # new_state = forward_looking_2(new_state, index, value)
            if new_state != None:
                result = backtrack(new_state)
                if result is not None:
                    return result
    return None

def solve(line):
    set_vars(line)
    state = generate_state(line)
    forward_looking(state)
    fin_state = backtrack(state)
    print_line(fin_state)

filename = sys.argv[1]
sudoku(filename)
# set_vars(".5A.2.789668.1.5.32.A6298.4.35135746.A8.9.85..32..421A..6...2..67.5.A38A.3.21647.96..3.4.15438.A9..2")
# print(constraint_sets)

# state = "............1234"
# solve(state)