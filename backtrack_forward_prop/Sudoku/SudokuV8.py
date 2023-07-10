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
    with open(filename) as f:
        lines = [line.strip() for line in f]
        lines.sort(key = lambda x : len(x))
        for line in lines[:15]:
            solve(line)

def check_puzzle(state):
    for symbol in symbol_set:
        if state.count(symbol) != N:
            print("PUZZLE IS WRONG")
            sys.exit()

def copy(state2):
    copy_of_state2 = {}
    for key in state2:
        copy_of_state2[(key[0], key[1])] = state2[key].copy()
    return copy_of_state2

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
        constraint_sets.append(frozenset({N * i + j for j in range(0, N)})) # rows
        constraint_sets.append(frozenset({N * j + i for j in range(0, N)})) # columns
    
    for w in range(0, N, subblock_width): # columns
        for h in range(0, N, subblock_height): # rows
            constraint_sets.append(frozenset({N * (i + h) + (w + j) for i in range(0, subblock_height) for j in range(0, subblock_width)})) # blocks

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
    state2 = {}
    for char in CHAR_STRING:
        for c_set in constraint_sets:
            indices = set()
            for val in c_set:
                if char in state[val]:
                    indices.add(val)
            state2[(char, c_set)] = indices
    return (state, state2)

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
            if smallest_length == 2:
                return var
    return var

def get_sorted_values(index, state):
    return state[index]

def forward_looking(new_state, state2):
    change = False

    one_solution_indices = deque([])
    for i in range(0, len(new_state)):
        if len(new_state[i]) == 1:
            one_solution_indices.append(i)
    
    while len(one_solution_indices) != 0:
        index = one_solution_indices.popleft()
        for neighbor in constraints[index]:
            if remove_item(new_state, state2, neighbor, new_state[index]):
                change = True
                # new_state, state2 = remove(new_state, state2, neighbor, new_state[index])
                if len(new_state[neighbor]) == 0:
                    return (None, None)
                elif len(new_state[neighbor]) == 1:
                    one_solution_indices.append(neighbor)
    
    if change:
        new_state, state2 = constraint_propagation(new_state, state2)
    
    return (new_state, state2)

def constraint_propagation(new_state, state2):
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
                return (None, None)
            elif count == 1:
                ind = new_state[index].index(value)
                remove_values = new_state[index][:ind] + new_state[index][ind + 1:]
                # print(remove_values)
                # new_state[index] = value
                # add state2 logic
                for val in remove_values:
                    # print((val, cset) in state2)
                    # print(index)
                    # print(state2[(val, cset)])
                    remove_item(new_state, state2, index, val)
                    # state2[(val, cset)].remove(index)
                change = True
    if change == True:
        new_state, state2 = forward_looking(new_state, state2)
    return (new_state, state2)

def place(state, state2, index, value):
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

    # add state2 logic
    for cset in constraint_sets_2[index]:
        for val in remove_values:
            state2[(val, cset)].remove(index)

    for char in remove_values:
        state, state2 = remove(state, state2, index, char) # removes values one by one
        if state is None:
            return (None, None)
    
    # forward looking on constraint sets
    for neighbor in constraints[index]:
        if value in state[neighbor]:
            remove_item(state, state2, neighbor, value)
            if len(state[neighbor]) == 0:
                return (None, None)
            state, state2 = remove(state, state2, neighbor, value)
            if state is None:
                return (None, None)
    
    return (state, state2)

def remove(state, state2, index, value):
    # check constraint propagation for three constraint sets
    for c_set in constraint_sets_2[index]:
        if len(state2[(value, c_set)]) == 1:
            state, state2 = place(state, state2, list(state2[(value, c_set)])[0], value)
        if state is None:
            return (None, None)
        # count = 0 # number of times that value appears in the set
        # ind = -1
        # for item in c_set:
        #     if value in state[item]:
        #         count += 1
        #         ind = item
        # if count == 0:
        #     return (None, None)
        # elif count == 1:
        #     if len(state[ind]) != 1:
        #         state, state2 = place(state, state2, ind, value)
        #     if state is None:
        #         return (None, None)

    # check if there are n squares with the exact same n values    
    n = len(state[index])
    # if n != 1:
    for c_set in constraint_sets_2[index]:
        indices = []
        for item in c_set:
            if state[item] == state[index]:
                indices.append(item)
        if len(indices) > n:
            return (None, None)
        elif len(indices) == n:
            remove_vals = [state[index][i] for i in range(0, n)]
            for item in c_set:
                if item not in indices:
                    for val in remove_vals:
                        if remove_item(state, state2, item, val):
                            state, state2 = remove(state, state2, item, val)
                            if state is None:
                                return (None, None)
    
    # check if there are x values that only occur in x squares
    # change to use state2 logic
    for cset in constraint_sets_2[index]:
        x = len(state2[value, cset])
        # if x != 1:
        values = set()
        for val in CHAR_STRING:
            if state2[val, cset] == state2[value, cset]:
                values.add(val)
        if len(values) > x:
            return (None, None)
        elif len(values) == x:
            copy_set = state2[value, cset].copy()
            for ind in copy_set:
                if ind in state2[value, cset]:
                    remove_values = []
                    for val in state[ind]:
                        if val not in values:
                            remove_values.append(val)
                    for val in remove_values:
                        if remove_item(state, state2, ind, val):
                            state, state2 = remove(state, state2, ind, val)
                        if state is None:
                            return (None, None)
    
    return (state, state2)

def remove_item(state, state2, index, val):
    if val in state[index]:
        ind = state[index].index(val)
        state[index] = state[index][:ind] + state[index][ind + 1:]
        for c_set in constraint_sets_2[index]:
            state2[(val, c_set)].remove(index)
        return True
    return False

def backtrack(state, state2):
    index = get_next_variable(state)
    if index == -1:
        return state
    if state is None:
        return (None, None)
    for value in get_sorted_values(index, state):
        new_state = state.copy()
        new_state2 = copy(state2)
        new_state, new_state2 = place(new_state, new_state2, index, value)
        if new_state is not None:
            result = backtrack(new_state, new_state2)
            if result[0] is not None:
                return result
    return (None, None)

def print_line(state): # takes a list of strings and prints it
    output = ""
    for item in state:
        output += item
    print(output)

def solve(line):
    set_vars(line)
    state, state2 = generate_state(line)
    # print_board(state)
    state, state2 = forward_looking(state, state2)
    # print_board(state)
    fin_state = backtrack(state, state2)
    print_line(fin_state)
    # print_board(fin_state)
    check_puzzle(fin_state)
    # number_of_instances(fin_state)

start = time.perf_counter()
filename = sys.argv[1]
sudoku(filename)
end = time.perf_counter()
print("Puzzles solved in %s seconds." % (end - start))

# solve(".143431212343421")