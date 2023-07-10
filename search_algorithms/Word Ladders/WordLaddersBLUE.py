from collections import deque
import time
import sys

# store words in a dictionary
# key = word
# value = [children of word]
def store_words(filename):
    words = {}
    with open(filename) as f:
        line_list = [line.strip() for line in f]
    for word in line_list:
        neighbors = []
        for w in words.keys():
            if apart_by_one_letter(word, w):
                neighbors.append(w)
                words[w].append(word)
        words[word] = neighbors
    return words

# tests if two words are apart by exactly one letter
# assume different words are passed in
def apart_by_one_letter(word1, word2):
    if len(word1) != len(word2):
        return False
    count = 0
    for i in range(0, len(word1)):
        if word1[i] != word2[i]:
            if count == 0:
                count = 1
            else:
                return False
    return True

# BiBFS algorithm
def BiBFS(word1, word2, words):
    reached_from_initial = {word1}
    reached_from_goal = {word2}
    queue_initial = deque([(word1, )])
    queue_goal = deque([(word2, )])

    while len(queue_initial) != 0 and len(queue_goal) != 0:
        # processing queue_initial
        state1 = queue_initial.popleft()
        if state1[0] in reached_from_goal:
            while len(queue_goal) != 0:
                path = queue_goal.popleft()
                if path[0] == state1[0]:
                    return state1[::-1] + path[1:]
        else:
            children = words[state1[0]]
            for child in children:
                if child not in reached_from_initial:
                    queue_initial.append((child, ) + state1)
                    reached_from_initial.add(child)

        # processing queue_goal
        state2 = queue_goal.popleft()
        if state2[0] in reached_from_initial:
            while len(queue_initial) != 0:
                path = queue_initial.popleft()
                if path[0] == state2[0]:
                    return path[::-1] + state2[1:]
        else: 
            children = words[state2[0]]
            for child in children:
                if child not in reached_from_goal:
                    queue_goal.append((child, ) + state2)
                    reached_from_goal.add(child)

    return None

# runs the whole program
def solve_puzzles(letters_file, puzzles_file):
    start = time.perf_counter()
    words = store_words(letters_file)
    end = time.perf_counter()
    print("Time to create the data structure was: %s seconds" % (end - start))
    print("There are %s words in this dict.\n" % len(words))
    print(words["blanks"])
    output = ""
    with open(puzzles_file) as f:
        line_list = [line.strip() for line in f]
    i = 0
    start = time.perf_counter()
    for line in line_list:
        puzzle = line.split()
        output += "Line: " + str(i) + "\n"
        tup = BiBFS(puzzle[0], puzzle[1], words)
        if tup == None:
            output += "No solution!\n\n"
        else:
            output += "Length is: " + str(len(tup)) + "\n"
            for word in tup:
                output += word + "\n"
            output += "\n"
        i += 1
    end = time.perf_counter()
    print(output)
    print("Time to solve all puzzles was: %s seconds" % (end - start))

# letters_file = sys.argv[1]
# puzzles_file = sys.argv[2]
# solve_puzzles(letters_file, puzzles_file)

# Debug
dictionary = store_words("words_test.txt")
# some_words = ['blinds', 'blinks', 'blanks', 'planks', 'planes', 'plates', 'plated', 'slated', 'seated', 'sealed', 'sealer', 'seller', 'teller', 'tiller', 'miller', 'milder', 'molder', 'molded']
# for i in range(0, len(some_words)):
#     print("Neighbors of " + some_words[i] + ": " + str(dictionary[some_words[i]]))
tup = BiBFS("blinds", "molded", dictionary)
print(tup)
print(len(tup))