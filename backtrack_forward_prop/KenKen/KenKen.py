# Isabella Zhu
# 10/05/21

# import statements
import sys
from heapq import heappush, heappop

# global variable defining size
N = 4
arithmetic_constraints = {}
pos_values = {}
row_col_constraints = {}

# helper recursive methods
def addition(size, val): # recursive
    global N
    if size == 0:
        return None
    elif size == 1 and val >= 1 and val <= N:
        return [(val, )]
    elif size == 1:
        return None
    ret_val = []
    for i in range(1, N + 1):
        temp = addition(size - 1, val - i)
        if temp != None:
            for item in temp:
                ret_val.append((i, ) + item)
    return ret_val

def multiplication(size, val): # recursive
    global N
    if size == 0:
        return None
    elif size == 1 and val >= 1 and val <= N:
        return [(val, )]
    elif size == 1:
        return None
    ret_val = []
    for i in range(1, N + 1):
        if val % i == 0:
            temp = multiplication(size - 1, val // i)
            if temp != None:
                for item in temp:
                    ret_val.append((i, ) + item)
    return ret_val

def subtraction(val): # not recursive
    ret_val = []
    for i in range(1, N + 1 - val):
        ret_val.append((i, i + val))
        ret_val.append((i + val, i))
    return ret_val

def division(val): # not recursive
    ret_val = []
    for i in range(1, N // val + 1):
        ret_val.append((i, i * val))
        ret_val.append((i * val, i))
    return ret_val

# methods for backtracking
def get_next_var(state):
    if len(state[1]) == 0:
        return None
    return state[1][len(state[1]) - 1]

def get_sorted_vals(var):
    global pos_values
    return pos_values[var]

def assign_values(state, var, val):
    global N, arithmetic_constraints, row_col_constraints
    dict = state[0]
    indices = arithmetic_constraints[var][2]
    for i in range(0, len(val)):
        if str(val[i]) not in dict[indices[i]]:
            return None
        dict[indices[i]] = str(val[i])
        for neighbor in row_col_constraints[indices[i]]:
            if str(val[i]) in dict[neighbor] and len(dict[neighbor]) == 1:
                return None
            elif str(val[i]) in dict[neighbor]:
                temp_ind = dict[neighbor].index(str(val[i]))
                dict[neighbor] = dict[neighbor][ : temp_ind] + dict[neighbor][temp_ind + 1 : ]
    return state
        

def backtrack(state):
    var = get_next_var(state)
    if var == None:
        return state
    for val in get_sorted_vals(var):
        new_state = (state[0].copy(), state[1].copy()[ : len(state[1]) - 1])
        new_state = assign_values(new_state, var, val)
        if new_state != None:
            final_state = backtrack(new_state)
            if final_state != None:
                return final_state
    return None

def gen_arithmetic_constraints(filename):
    global N, arithmetic_constraints
    with open(filename) as f:
        lines = [line.strip() for line in f]
        puzzle = lines[0]
        N = int(len(puzzle) ** 0.5)

        for i in range(0, len(puzzle)):
            letter = puzzle[i]
            if letter not in arithmetic_constraints:
                arithmetic_constraints[letter] = [i, ]
            else:
                arithmetic_constraints[letter].append(i)
        
        for line in lines[1 : ]:
            chars = line.split()
            letter = chars[0]
            num = int(chars[1])
            op = chars[2]
            arithmetic_constraints[letter] = (num, op, arithmetic_constraints[letter])

def gen_possible_values():
    global N, arithmetic_constraints, pos_values
    for letter, tup in arithmetic_constraints.items():
        num, op, indices = tup
        constraint_list = []
        if op == "+":
            constraint_list = addition(len(indices), num)
        elif op == "x":
            constraint_list = multiplication(len(indices), num)
        elif op == "-":
            constraint_list = subtraction(num)
        elif op == "/":
            constraint_list = division(num)
        else:
            print("wrong operation")
        pos_values[letter] = constraint_list

def gen_row_col_constraints():
    global N, row_col_constraints
    for i in range(0, N * N):
        a = i // N
        b = i % N
        constraints = []
        for j in range(0, N): # rows first
            if a != j:
                constraints.append(N * j + b)
        for j in range(0, N): # columns next
            if b != j:
                constraints.append(N * a + j)
        row_col_constraints[i] = constraints
        # print(str(i) + ": " + str(constraints))

def solve(filename):
    global N, pos_values

    gen_arithmetic_constraints(filename)
    gen_possible_values()
    gen_row_col_constraints()
    
    # generate start state
    start_dict = {}
    start_list = []

    string = ""
    for j in range(1, N + 1):
        string += str(j)
    for i in range(0, N * N):
        start_dict[i] = string
    
    for letter in pos_values:
        start_list.append(letter)
    
    start_list.sort(key = lambda letter : -1 * len(pos_values[letter]))

    final_state = backtrack((start_dict, start_list))

    output = ""
    for i in final_state[0]:
        output += str(final_state[0][i])
    print(output)

solve(sys.argv[1])
    
    