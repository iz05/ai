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

# board will be stored as a list of strings, each string stores all possibilities of characters

def sudoku(filename):
    with open(filename) as f:
        lines = [line.strip() for line in f]
        for line in lines:
            solve(line)


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
        for s in constraint_sets:
            if i in s:
                constraints[i].update(s)
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

def forward_looking(state):
    new_state = state.copy()
    one_solution_indices = deque([])
    for i in range(0, len(new_state)):
        if len(new_state[i]) == 1:
            one_solution_indices.append(i)
    
    while len(one_solution_indices) != 0:
        index = one_solution_indices.popleft()
        for neighbor in constraints[index]:
            if new_state[index] in new_state[neighbor]:
                i = new_state[neighbor].find(new_state[index])
                new_state[neighbor] = new_state[neighbor][ : i] + new_state[neighbor][i + 1 :]
                if len(new_state[neighbor]) == 0:
                    return None
                elif len(new_state[neighbor]) == 1:
                    one_solution_indices.append(neighbor)
    
    return new_state

def backtrack(state):
    index = get_next_variable(state)
    if index == -1:
        return state
    for value in get_sorted_values(index, state):
        new_state = state.copy()
        new_state[index] = value
        new_state = forward_looking(new_state)
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
    state = forward_looking(state)
    fin_state = backtrack(state)
    print_line(fin_state)

filename = sys.argv[1]
sudoku(filename)
# set_vars(".5A.2.789668.1.5.32.A6298.4.35135746.A8.9.85..32..421A..6...2..67.5.A38A.3.21647.96..3.4.15438.A9..2")
# print(constraint_sets)

# state = ".432321441232341"
# solve(state)