import sys

# three player game instead of two player

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

def win(cur): # returns 1 if player will win, returns -1 if player will lose
    if cur in legal_words:
        return -1
    for move in possible_moves(cur):
        if cur + move not in legal_words: # second player tries not to make a word
            for move2 in possible_moves(cur + move):
                if cur + move + move2 not in legal_words: # third player tries not to make a word
                    m = -1
                    for move3 in possible_moves(cur + move + move2): # first player tries to make moves
                        m = max(m, win(cur + move + move2 + move3))
                    if m == -1:
                        return -1
    return 1         

def victory_moves(start): # prints a list of the moves we can make to guarantee victory
    moves = []
    for move in possible_moves(start):
        if win(start + move) == 1:
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