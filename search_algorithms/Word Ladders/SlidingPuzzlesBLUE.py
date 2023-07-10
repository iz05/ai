import time
import sys

# store words in a dictionary
# key = word
# value = [children of word]
def store_words(filename):
    words = []
    
    return

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
def BiBFS(word1, word2):
    return

# runs the whole program
def solve_puzzles(letters_file, puzzles_file):
    return

letters_file = sys.argv[1]
puzzles_file = sys.argv[2]
solve_puzzles(letters_file, puzzles_file)