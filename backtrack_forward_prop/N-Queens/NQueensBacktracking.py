# Isabella Zhu
# N-Queens Backtracking

import time
import random

N = 40

def test_solution(state):
    for var in range(len(state)):
        left = state[var]
        middle = state[var]
        right = state[var]
        for compare in range(var + 1, len(state)):
            left -= 1
            right += 1
            if state[compare] == middle:
                print(var, "middle", compare)
                return False
            if left >= 0 and state[compare] == left:
                print(var, "left", compare)
                return False
            if right < len(state) and state[compare] == right:
                print(var, "right", compare)
                return False
    return True

# VERSION 1

# def goal_test(state):
#     # check if all rows are occupied
#     if len(state) != N:
#         return False

#     # check columns
#     if len(set(state)) != N:
#         return False
    
#     # check diagonals
#     for i in range(0, N):
#         for j in range(i + 1, N):
#             if j + state[j] == i + state[i] or state[j] - j == state[i] - i:
#                 return False

#     return True

# def get_next_unassigned_var(state):
#     return len(state)

# def get_sorted_values(state, var):
#     return [i for i in range(0, N)]

# def csp_backtracking(state):
#     if goal_test(state):
#         return state
#     elif len(state) == N:
#         return None
#     var = get_next_unassigned_var(state)
#     for val in get_sorted_values(state, var):
#         new_state = state.copy()
#         new_state.append(val)
#         result = csp_backtracking(new_state)
#         if result is not None:
#             return result
#     return None







# VERSION 2

# def conflict(state, row, val):
#     # only need to check i
#     for i in range(0, row):
#         if state[i] + i == row + val or state[i] - i == val - row or state[i] == val:
#             return True
#     return False

# def get_next_unassigned_var(state):
#     return len(state)

# def get_sorted_values(state, var):
#     return [i for i in range(0, N) if not conflict(state, var, i)]

# def csp_backtracking(state):
#     if len(state) == N:
#         return state
#     var = get_next_unassigned_var(state)
#     for val in get_sorted_values(state, var):
#         new_state = state.copy()
#         new_state.append(val)
#         result = csp_backtracking(new_state)
#         if result is not None:
#             return result
#     return None



# VERSION 3

# state is a tuple: (list of queens, set of right diagonal sums, set of left diagonal sums, set of columns)

def conflict(state, row, val):
    # only need to check i
    if row + val in state[1] or val - row in state[2] or val in state[3]:
        return True
    return False
    
def get_next_unassigned_var(state):
    return len(state[0])

def get_sorted_values(state, var):
    vals = []
    for i in range(0, N):
        if not conflict(state, var, i):
            vals.append(i)
    random.shuffle(vals)
    return vals
    # if var % 2 == 1:
    #     return [i for i in range(N - 1, -1, -1) if not conflict(state, var, i)]
    # return [i for i in range(0, N) if not conflict(state, var, i)]

def csp_backtracking(state):
    if len(state[0]) == N:
        return state
    var = get_next_unassigned_var(state)
    for val in get_sorted_values(state, var):
        new_state = (
            state[0].copy(),
            state[1].copy(),
            state[2].copy(),
            state[3].copy(),
        )
        new_state[0].append(val)
        new_state[1].add(var + val)
        new_state[2].add(val - var)
        new_state[3].add(val)
        result = csp_backtracking(new_state)
        if result is not None:
            return result
    return None

start = time.perf_counter()
for i in range(8, 201):
    N = i
    sol = csp_backtracking(([], set(), set(), set()))[0]
    print("Solution for N = %s finished generating." % i)
    if test_solution(sol):
        print("Solution is correct\n")
    else:
        print("Solution is wrong\n")
end = time.perf_counter()
print("Total time: %s seconds" % (end - start))