from collections import deque
import time
import sys

# code is used for both BLUE and RED Option 1 assignments

# store words in a dictionary
# key = word
# value = [children of word]
def store_words(filename):
    words = {}
    temp_dict = {}
    with open(filename) as f:
        line_list = [line.strip() for line in f]
    for word in line_list:
        words[word] = set()
        for i in range(len(word)):
            template = word[:i] + "." + word[i + 1:]
            if template in temp_dict:
                temp_dict[template].add(word)
            else:
                temp_dict[template] = {word}
    for bucket, neighbors in temp_dict.items():
        for word1 in neighbors:
            for word2 in neighbors:
                if word1 != word2:
                    words[word1].add(word2)
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
# assume word1 not equal to word2
def BiBFS(word1, word2, words):
    reached_from_initial = {word1}
    reached_from_goal = {word2}
    queue_initial = deque([(word1, )])
    queue_goal = deque([(word2, )])

    while len(queue_initial) != 0 and len(queue_goal) != 0:
        # processing queue_initial
        size_initial = len(queue_initial)
        for i in range(0, size_initial):
            state1 = queue_initial.popleft()
            children = words[state1[0]]
            for child in children:
                if child in reached_from_goal:
                    while len(queue_goal) != 0:
                        path = queue_goal.popleft()
                        if path[0] == child:
                            return state1[::-1] + path
                elif child not in reached_from_initial:
                    queue_initial.append((child, ) + state1)
                    reached_from_initial.add(child)

        # processing queue_goal
        size_goal = len(queue_goal)
        for i in range(0, size_goal):
            state2 = queue_goal.popleft()
            children = words[state2[0]]
            for child in children:
                if child in reached_from_initial:
                    while len(queue_initial) != 0:
                        path = queue_initial.popleft()
                        if path[0] == child:
                            return path[::-1] + state2
                elif child not in reached_from_goal:
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

def answer_questions(letters_file):
    neighbors = store_words(letters_file)

    max_connected = set()
    graph = []
    words = set()
    for item in neighbors.keys():
        words.add(item)

    single_count = 0

    while len(words) != 0:
        word = words.pop()
        component = {word} # essentially the visited set
        queue = deque([word])
        while len(queue) != 0:
            temp = queue.popleft()
            for child in neighbors[temp]:
                if child not in component:
                    words.remove(child)
                    component.add(child)
                    queue.append(child)
        if len(component) > len(max_connected):
            max_connected = component

        if len(component) > 1:
            graph.append(component)
        else:
            single_count += 1
    
    print("Question 1: There are %s singletons." % single_count)
    print("Question 2: There are %s words in the largest connected subcomponent." % len(max_connected))
    print("Question 3: There are %s connected subcomponents." % len(graph))

    longest_path = ()
    for word1 in max_connected:
        for word2 in max_connected:
            if word1 > word2:
                path = BiBFS(word1, word2, neighbors)
                if len(path) > len(longest_path):
                    longest_path = path
    print("Question 4: The longest word ladder has length %s." % len(longest_path))
    print("An example of such a path is: " + str(longest_path))

letters_file = sys.argv[1]
puzzles_file = sys.argv[2]
# answer_questions(letters_file)
solve_puzzles(letters_file, puzzles_file)

# Debug
# dictionary = store_words("words_06_letters.txt")
# tup = BiBFS("blinds", "molded", dictionary)
# print(tup)
# print(len(tup))