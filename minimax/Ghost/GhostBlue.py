import sys

legal_words = set() # formatting: everything in upper case, set of all legal words
legal_starts = {} # keys are starts of words (but not a complete word) 

def read_file(filename, minimum_word_length):
    with open(filename) as f:
        words = [line.strip() for line in f]
        for word in words:
            if word.isalpha() and len(word) >= minimum_word_length:
                legal_words.add(word.upper())
                for i in range(1, len(word)):
                    sub = word.upper()[0 : i]
                    if sub not in legal_starts:
                        legal_starts[sub] = set()
                    legal_starts[sub].add(word.upper())
        legal_starts[""] = set()
        for word in legal_words:
            legal_starts[""].add(word)
            if word in legal_starts:
                del legal_starts[word]

def possible_moves(start): # returns all moves that will not make a word, assumption: start is not a word
    moves = set() # a set of letters
    for word in legal_starts[start]:
        moves.add(word[len(start)])
    return moves

def victory(cur): # returns true if guaranteed victory, returns false otherwise
    if cur in legal_words:
        return True
    for move in possible_moves(cur):
        new_cur = cur + move
        if not victory(new_cur): # if opponent cannot guarantee victory, then we win 
            return True
    return False # if opponent can guarantee victory no matter what move we make, then we lose

def victory_moves(start): # prints a list of the moves we can make to guarantee victory
    moves = []
    for move in possible_moves(start):
        if not victory(start + move):
            moves.append(move)
    if len(moves) > 0:
        print("Next player can guarantee victory by playing any of these letters: " + str(moves))
    else:
        print("Next player will lose!")

read_file(sys.argv[1].upper(), int(sys.argv[2]))
start = ""
if len(sys.argv) > 3:
    start = sys.argv[3]
victory_moves(start)