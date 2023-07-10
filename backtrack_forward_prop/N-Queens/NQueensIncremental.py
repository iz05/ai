# Isabella Zhu
import time
import random

N = 40
random.seed(time.time()) # ensures random numbers every time

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

def generate_state(): # returns a random (most likely flawed) state
    state = []
    val = N // 2
    # for i in range(0, N):
    #     state.append(random.randint(0, N - 1))
    # return state
    for i in range(0, N):
        state.append(val)
        val = (val + 2) % N
    return state

def most_conflicted(state): # returns an index that has the most conflicts (random if there is a tie)
    max_conflicts = 0
    max_indices = []
    total_conflicts = 0
    for i in range(0, N):
        conflicts = 0
        for j in range(0, N):
            if state[i] == state[j] or state[i] + i == state[j] + j or state[i] - i == state[j] - j:
                conflicts += 1
        conflicts -= 1
        total_conflicts += conflicts
        if max_conflicts < conflicts:
            max_indices.clear()
            max_indices.append(i)
            max_conflicts = conflicts
        elif max_conflicts == conflicts:
            max_indices.append(i)
    return (total_conflicts // 2, max_indices[random.randint(0, len(max_indices) - 1)])

def better_state(state, index): # returns a state with the queen in row index moved to a spot with the least number of conflicts (random if there is a tie)
    min_conflicts = N # can't have N conflicts
    min_indices = []
    for i in range(0, N):
        conflicts = 0
        for j in range(0, N):
            if i == state[j] or i + index == state[j] + j or i - index == state[j] - j:
                conflicts += 1
        conflicts -= 1
        if min_conflicts > conflicts:
            min_indices.clear()
            min_indices.append(i)
            min_conflicts = conflicts
        elif min_conflicts == conflicts:
            min_indices.append(i)
    new_index = random.randint(0, len(min_indices) - 1)
    state[index] = min_indices[new_index]
    return state

# def increment():
#     start = time.perf_counter()
#     print("Size N = %s" % N)
#     state = generate_state()
#     while(True):
#         conflicts, x = most_conflicted(state)
#         print("State %s has %s conflicts." % (state, conflicts))
#         if conflicts == 0:
#             end = time.perf_counter()
#             print("Time taken: %s seconds" % (end - start))
#             return state
#         state = better_state(state, x)
def increment():
    print("Size N = %s" % N)
    state = generate_state()
    while(True):
        conflicts, x = most_conflicted(state)
        # print("State %s has %s conflicts." % (state, conflicts))
        if conflicts == 0:
            return state
        state = better_state(state, x)

# start = time.perf_counter() # keeps track of total time

# state = increment()
# if test_solution(state):
#     print("Solution is correct\n")
# else:
#     print("Solution is incorrect\n")

# N = 50
# state = increment()
# if test_solution(state):
#     print("Solution is correct\n")
# else:
#     print("Solution is incorrect\n")

# end = time.perf_counter() # keeps track of total time
# print("Total time taken to solve: %s seconds" % (end - start))

# attempting the extension lol
start = time.perf_counter()
for i in range(8, 201):
    N = i
    state = increment()
    print("Finished for N = %s" % N)
end = time.perf_counter()
print("Total time: %s seconds" % (end - start))