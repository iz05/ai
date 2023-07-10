# Isabella Zhu

import sys

N = 0
subblock_height = 0
subblock_width = 0
symbol_set = None
constraint_sets = [] # 3N sets of constraints, N for rows, N for columns, N for subgrids
constraints = {} # key = index of square, value = set of neighbors

def sudoku(filename):
    with open(filename) as f:
        lines = [line.strip() for line in f]
        for line in lines:
            solve(line)

def set_vars(state):
    global N, subblock_height, subblock_width, symbol_set, constraint_sets, constraints
    constraint_sets = []
    constraints = {}

    N = int(len(state) ** 0.5)

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
    return state.index(".")

def get_sorted_values(index, state):
    global symbol_set, constraints
    used_values = set()
    for i in constraints[index]:
        if state[i] != ".":
            used_values.add(state[i])
    return symbol_set - used_values

def backtrack(state):
    if state.find(".") == -1:
        return state
    index = get_next_variable(state)
    for value in get_sorted_values(index, state):
        new_state = state[ : index] + value + state[index + 1 : ]
        result = backtrack(new_state)
        if result is not None:
            return result
    return None

def solve(state):
    set_vars(state)
    print(backtrack(state))

filename = sys.argv[1]
sudoku(filename)
# set_vars(".5A.2.789668.1.5.32.A6298.4.35135746.A8.9.85..32..421A..6...2..67.5.A38A.3.21647.96..3.4.15438.A9..2")
# print(constraint_sets)