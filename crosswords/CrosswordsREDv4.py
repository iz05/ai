import sys; args = sys.argv[1:]
myLines = open(args[0], 'r').read().splitlines()

import time, math, random, re

# version 4: improved data processing

# variables
width = 0
height = 0
puzzle = []
words = set()
blocks = 0
blanks = 0
squares = set()
horizontal = {}
vertical = {}
word_bank = {}
h_neighbors = {}
v_neighbors = {}
words_by_size = {}
templates_in_options = set()
options_global = {}
SIZE = 9
THRESHOLD = 6

def process_input(): # reads in data
    global width, height, puzzle, words, blocks
    dim = args[1].split("x")
    height = int(dim[0])
    width = int(dim[1])
    blocks = int(args[2])

    # all possible positions
    for i in range(0, height):
        for j in range(0, width):
            squares.add((i, j))
    
    for i in range(0, height):
        puzzle.append("." * width)

    for line in myLines:
        if line.isalpha() and len(line) >= 3:
            words.add(line.upper())

    # processing all other data
    for i in range(3, len(args)):
        data = args[i]
        orientation = data[0]
        data = data[1 : ]
        ind = data.find("x")
        row = int(data[0 : ind])
        temp = data[ind + 1: ]
        num = ""
        for i in range(0, len(temp)):
            if temp[i] in "0123456789":
                num += temp[i]
            else:
                break
        col = int(num)
        word = temp[len(num) : ]
        for char in word:
            if char.isalpha():
                char = char.upper()
            puzzle[row] = puzzle[row][0 : col] + char + puzzle[row][col + 1 : ]
            if orientation == "V" or orientation == "v":
                row += 1
            elif orientation == "H" or orientation == "h":
                col += 1
            else:
                print("Error while processing input")
        if len(word) == 0:
            puzzle[row] = puzzle[row][0 : col] + "#" + puzzle[row][col + 1 : ]

def print_board(puzzle):
    s = ""
    for line in puzzle:
        for char in line:
            s += char + " "
        s += "\n"
    print(s)

# build methods 

def area_fill(puzzle, x, y): # fills all blank spaces it can with the letter A
    place_square("A", puzzle, x, y)
    if x - 1 >= 0 and puzzle[x - 1][y] != "A" and puzzle[x - 1][y] != "#":
        area_fill(puzzle, x - 1, y)
    if x + 1 < height and puzzle[x + 1][y] != "A" and puzzle[x + 1][y] != "#":
        area_fill(puzzle, x + 1, y)
    if y - 1 >= 0 and puzzle[x][y - 1] != "A" and puzzle[x][y - 1] != "#":
        area_fill(puzzle, x, y - 1)
    if y + 1 < width and puzzle[x][y + 1] != "A" and puzzle[x][y + 1] != "#":
        area_fill(puzzle, x, y + 1)

def check_area_fill(state):
    puzzle, block_squares, blank_squares = state
    if len(block_squares) == width * height: return False
    temp = squares - block_squares
    puzzle2 = puzzle.copy()
    blank = next(iter(temp))
    area_fill(puzzle2, blank[0], blank[1]) 
    for i in range(0, height):
        for j in range(0, width):
            if puzzle2[i][j] != "#" and puzzle2[i][j] != "A":
                return False
    return True

def valid_blocking(state):
    puzzle, block_squares, blank_squares = state
    blank_squares = squares - block_squares
    
    # Condition 1: every space on the board must be part of a horizontal word and a vertical word
    for square in blank_squares:
        r, c = square
        if (r - 1, c) not in blank_squares and (r + 1, c) not in blank_squares or (r, c - 1) not in blank_squares and (r, c + 1) not in blank_squares:
            return False
    
    # Condition 2: every word must be at least 3 characters long
    for square in block_squares:
        r, c = square
        if (r - 1, c) in blank_squares:
            if (r - 2, c) not in blank_squares or (r - 3, c) not in blank_squares:
                return False
        if (r + 1, c) in blank_squares:
            if (r + 2, c) not in blank_squares or (r + 3, c) not in blank_squares:
                return False
        if (r, c - 1) in blank_squares:
            if (r, c - 2) not in blank_squares or (r, c - 3) not in blank_squares:
                return False
        if (r, c + 1) in blank_squares:
            if (r, c + 2) not in blank_squares or (r, c + 3) not in blank_squares:
                return False
    
    # Condition 3 : the board is 180 degree rotationally symmetric
    for i in range(0, height):
        for j in range(0, width):
            i2 = height - i - 1
            j2 = width - j - 1
            if puzzle[i][j] == "#":
                if puzzle[i2][j2] != "#":
                    return False
    
    # Condition 4: all the spaces must form one connected block
    if check_area_fill(state) == False:
        return False
    
    return True  

def forward_looking(state): 
    puzzle, block_squares, blank_squares = state
    block_squares = block_squares.copy()
    blank_squares = blank_squares.copy()
    for square in blank_squares:
        row, col = square
        if (row, col - 1) in block_squares or out_of_bounds((row, col - 1)):
            state = place_and_update("-", state, row, col + 1)
            if state == False: return None
            state = place_and_update("-", state, row, col + 2)
            if state == False: return None
        if (row, col + 1) in block_squares or out_of_bounds((row, col + 1)):
            state = place_and_update("-", state, row, col - 1)
            if state == False: return None
            state = place_and_update("-", state, row, col - 2)
            if state == False: return None
        if (row - 1, col) in block_squares or out_of_bounds((row - 1, col)):
            state = place_and_update("-", state, row + 1, col)
            if state == False: return None
            state = place_and_update("-", state, row + 2, col)
            if state == False: return None
        if (row + 1, col) in block_squares or out_of_bounds((row + 1, col)):
            state = place_and_update("-", state, row - 1, col)
            if state == False: return None
            state = place_and_update("-", state, row - 2, col)
            if state == False: return None
    for square in block_squares:
        row, col = square
        if (row, col + 1) in block_squares or out_of_bounds((row, col + 1)): pass
        elif (row, col + 2) in block_squares or out_of_bounds((row, col + 2)):
            state = place_and_update("#", state, row, col + 1)
            if state == False: return None
        elif (row, col + 3) in block_squares or out_of_bounds((row, col + 3)):
            state = place_and_update("#", state, row, col + 1)
            if state == False: return None
            state = place_and_update("#", state, row, col + 2)
            if state == False: return None
        if (row, col - 1) in block_squares or out_of_bounds((row, col - 1)): pass
        elif (row, col - 2) in block_squares or out_of_bounds((row, col - 2)):
            state = place_and_update("#", state, row, col - 1)
            if state == False: return None
        elif (row, col - 3) in block_squares or out_of_bounds((row, col - 3)):
            state = place_and_update("#", state, row, col - 1)
            if state == False: return None
            state = place_and_update("#", state, row, col - 2)
            if state == False: return None
        if (row - 1, col) in block_squares or out_of_bounds((row - 1, col)): pass
        elif (row - 2, col) in block_squares or out_of_bounds((row - 2, col)):
            state = place_and_update("#", state, row - 1, col)
            if state == False: return None
        elif (row - 3, col) in block_squares or out_of_bounds((row - 3, col)):
            state = place_and_update("#", state, row - 1, col)
            if state == False: return None
            state = place_and_update("#", state, row - 2, col)
            if state == False: return None
    if not(block_squares == state[1] and blank_squares == state[2]):
        state = forward_looking(state)
    return state

def place_square(token, puzzle, row, col):
    puzzle[row] = puzzle[row][ : col] + token + puzzle[row][col + 1 : ]

def place_and_update(token, state, row, col): # returns an updated state, returns False if impossible to place
    puzzle, block_squares, blank_squares = state
    if not out_of_bounds((row, col)):
        if token == "#" and (puzzle[row][col] == "-" or puzzle[row][col].isalpha()): return False
        if token == "-" and puzzle[row][col] == "#": return False
        if token == "#" and puzzle[row][col] == "#": return state
        if token == "-" and (puzzle[row][col] == "-" or puzzle[row][col].isalpha()): return state
        place_square(token, puzzle, row, col)
        place_square(token, puzzle, height - 1 - row, width - 1 - col)
        if token == "#":
            block_squares.add((row, col))
            block_squares.add((height - 1 - row, width - 1 - col))
        elif token == "-":
            blank_squares.add((row, col))
            blank_squares.add((height - 1 - row, width - 1 - col))
        return (puzzle, block_squares, blank_squares)
    return False

def out_of_bounds(tup):
    row, col = tup
    return not(row >= 0 and row < height and col >= 0 and col < width)

def get_spaces(state):
    spaces = squares.difference(state[1]).difference(state[2])
    spaces = list(spaces)
    spaces.sort(key = lambda s : -1 * heuristic(s, state))
    return spaces # returns all squares with "."

def heuristic(space, state): # product of length of words
    new_state = (state[0].copy(), state[1].copy(), state[2].copy())
    new_state = place_and_update("#", new_state, space[0], space[1])
    puzzle = new_state[0]
    product = 1
    for r in range(0, len(puzzle)):
        word = ""
        for c in range(0, len(puzzle[0])):
            if puzzle[r][c] == "#":
                if len(word) != 0:
                    product *= len(word)
                    word = ""
            else:
                word += puzzle[r][c]
        if puzzle[r][len(puzzle[0]) - 1] != "#":
            product *= len(word)

    for c in range(0, len(puzzle[0])):
        word = ""
        for r in range(0, len(puzzle)):
            if puzzle[r][c] == "#":
                if len(word) != 0:
                    product *= len(word)
                    word = ""
            else:
                word += puzzle[r][c]
        if puzzle[len(puzzle) - 1][c] != "#":
            product *= len(word)
    return product

def backtrack(state, b): # returns a valid blocking of a puzzle
    if b and not valid_blocking(state): return None
    puzzle, block_squares, blank_squares = state
    if len(block_squares) > blocks:
        return None
    if len(block_squares) == blocks:
        for i in range(0, height):
            for j in range(0, width):
                if puzzle[i][j] == ".":
                    state = place_and_update("-", state, i, j)
        if valid_blocking(state):
            return state
        else:
            return None
    for space in get_spaces(state):
        row, col = space
        new_state = (puzzle.copy(), block_squares.copy(), blank_squares.copy())
        new_state = place_and_update("#", new_state, row, col)
        new_state = forward_looking(new_state)
        if new_state is not None:
            new_puzzle = backtrack(new_state, True)
            if new_puzzle is not None:
                return new_puzzle
    return None

def build(): # returns the built puzzle
    global width, height, puzzle, words, blocks, blanks

    if blocks == height * width: # special case: all squares are blocked
        puzzle = []
        for i in range(0, height):
            puzzle.append("#" * width)
        return puzzle
    
    for r in range(0, height): # preserves rotational symmetry
        for c in range(0, width):
            r2 = height - r - 1
            c2 = width - c - 1
            if puzzle[r][c] == "#":
                puzzle[r2] = puzzle[r2][ : c2] + "#" + puzzle[r2][c2 + 1 : ]
            elif puzzle[r][c].isalpha() or puzzle[r][c] == "-":
                if not puzzle[r2][c2].isalpha():
                    puzzle[r2] = puzzle[r2][ : c2] + "-" + puzzle[r2][c2 + 1 : ]
    
    if blocks % 2 == 1: # if number of blocks is odd, then center space is a block
        puzzle[(height - 1) // 2] = puzzle[(height - 1) // 2][ : (width - 1) // 2] + "#" + puzzle[(height - 1) // 2][(width + 1) // 2 : ]
    if blocks % 2 == 0 and width % 2 == 1 and height % 2 == 1:
        if puzzle[(height - 1) // 2][(width - 1) // 2] == ".":
            puzzle[(height - 1) // 2] = puzzle[(height - 1) // 2][ : (width - 1) // 2] + "-" + puzzle[(height - 1) // 2][(width + 1) // 2 : ]
    
    block_squares = set()
    blank_squares = set()
    for r in range(0, height):
        for c in range(0, width):
            if puzzle[r][c] == "#":
                block_squares.add((r, c))
            elif puzzle[r][c] == "-" or puzzle[r][c].isalpha():
                blank_squares.add((r, c))
    
    blanks = width * height - blocks
    
    state = (puzzle, block_squares, blank_squares)
    state = backtrack(state, False)
    if state is None:
        print("Impossible to block.")
    else:
        for i in range(0, len(puzzle)):
            for j in range(0, len(puzzle[i])):
                if puzzle[i][j] == ".":
                    puzzle[i] = puzzle[i][ : j] + "-" + puzzle[i][j + 1 :]
        return state

# FILL METHODS 

def generate_data(state): # fills horizontal, vertical
    global horizontal, vertical, word_bank, h_neighbors, v_neighbors, words_by_size, templates_in_options, options_global
    puzzle, block_squares, blank_squares = state
    positions = set() # set of positions that are still blank
    words_used = set()

    # fills in the four global dictionaries
    for space in blank_squares:
        row, col = space
        h_neighbors[space] = set()
        i = -1
        while (row, col + i) in blank_squares:
            h_neighbors[space].add((row, col + i))
            i = i - 1
        pos = -1 * i - 1
        i = 1
        while (row, col + i) in blank_squares:
            h_neighbors[space].add((row, col + i))
            i = i + 1
        length = pos + i
        horizontal[space] = (length, pos)

        v_neighbors[space] = set()
        i = -1
        while (row + i, col) in blank_squares:
            v_neighbors[space].add((row + i, col))
            i = i - 1
        pos = -1 * i - 1
        i = 1
        while (row + i, col) in blank_squares:
            v_neighbors[space].add((row + i, col))
            i = i + 1
        length = pos + i
        vertical[space] = (length, pos)

        if puzzle[row][col] == "-":
            positions.add(space)
    
    for i in range(3, SIZE + 1):
        words_by_size[i] = set()

    # fills in word_bank
    for word in words:
        if len(word) <= SIZE:
            words_by_size[len(word)].add(word)
        if len(word) <= THRESHOLD:
            templates = helper_recur(word, 0)
            for template in templates:
                if template not in word_bank:
                    word_bank[template] = set()
                word_bank[template].add(word)

    # for i in range(THRESHOLD + 1, SIZE + 1):
    #     template = "-" * i
    #     word_bank[template] = words_by_size[i].copy()
    
    for blank in blank_squares:
        word = get_h_word(puzzle, blank)
        if word.find("-") == -1:
            words_used.add(word)
        word = get_v_word(puzzle, blank)
        if word.find("-") == -1:
            words_used.add(word)
    
    options = {}
    for blank in blank_squares:
        options[blank] = get_options(puzzle, blank)

    return (puzzle, positions, words_used, options)

def fit(template, word):
    if len(template) != len(word):
        return False
    for i in range(0, len(template)):
        if template[i] != "-" and template[i] != word[i]:
            return False
    return True

def to_string(set):
    output = ""
    for thing in set:
        output += thing
    return output

def to_set(string):
    output = set()
    for char in string:
        output.add(char)
    return output

def helper_recur(word, index):
    ret = set()
    if index == len(word) - 1:
        ret.add("-")
        ret.add(word[-1])
        return ret
    temp = helper_recur(word, index + 1)
    for thing in temp:
        ret.add(word[index] + thing)
        ret.add("-" + thing)
    return ret

def get_h_word(puzzle, blank):
    row, col = blank
    length, pos = horizontal[blank]
    word = ""
    for i in range(0, pos + 1):
        word = puzzle[row][col - i] + word
    for i in range(1, length - pos):
        word = word + puzzle[row][col + i]
    return word

def get_v_word(puzzle, blank):
    row, col = blank
    length, pos = vertical[blank]
    word = ""
    for i in range(0, pos + 1):
        word = puzzle[row - i][col] + word
    for i in range(1, length - pos):
        word = word + puzzle[row + i][col]
    return word

def get_options(puzzle, blank):
    h_word = get_h_word(puzzle, blank)
    if h_word not in word_bank:
        possible_words_h = set()
        for word in words_by_size[len(h_word)]:
            if fit(h_word, word):
                possible_words_h.add(word)
        word_bank[h_word] = possible_words_h
    letters_h = set()
    position_h = horizontal[blank][1]
    for word in word_bank[h_word]:
        letters_h.add(word[position_h])
    v_word = get_v_word(puzzle, blank)
    if v_word not in word_bank:
        possible_words_v = set()
        for word in words_by_size[len(v_word)]:
            if fit(v_word, word):
                possible_words_v.add(word)
        word_bank[v_word] = possible_words_v
    letters_v = set()
    position_v = vertical[blank][1]
    for word in word_bank[v_word]:
        letters_v.add(word[position_v])
    return frozenset(letters_h.intersection(letters_v))

def place_and_update_fill(state, blank, letter):
    puzzle, positions, words_used, options = state
    row, col = blank
    puzzle[row] = puzzle[row][ : col] + letter + puzzle[row][col + 1 : ] # update puzzle
    positions.remove(blank) # update positions
    h_word = get_h_word(puzzle, blank) # update words_used
    if h_word.find("-") == -1:
        if h_word not in words or h_word in words_used:
            return None
        words_used.add(h_word)
    v_word = get_v_word(puzzle, blank) # update words_used
    if v_word.find("-") == -1:
        if v_word not in words or v_word in words_used:
            return None
        words_used.add(v_word)
    del options[blank] # update options
    for h in h_neighbors[blank]:
        if h in options:
            options[h] = get_options(puzzle, h)
    for v in v_neighbors[blank]:
        if v in options:
            options[v] = get_options(puzzle, v)
    return state

def forward_looking_fill(state):
    puzzle, positions, words_used, options = state
    blanks = positions.copy()
    flag = False # False if changes were not made, True if changes were made
    for blank in blanks:
        if len(options[blank]) == 0:
            return None
        elif len(options[blank]) == 1:
            for x in options[blank]:
                state = place_and_update_fill(state, blank, x)
            flag = True
            if state is None:
                return None
    if flag == True:
        state = forward_looking_fill(state)
    return state

def get_var(state):
    options = state[3]
    min_var = None
    min_set = None
    min_size = 27
    for blank in state[1]:
        if len(options[blank]) < min_size:
            min_var = blank
            min_set = options[blank]
            min_size = len(options[blank])
    return (min_var, min_set)

def backtrack_fill(state):
    puzzle, positions, words_used, options = state
    if len(positions) == 0:
        return state
    if state is not None:
        var = get_var(state)
        if var is not None:
            blank, letters = var
            for letter in letters:
                new_state = (puzzle.copy(), positions.copy(), words_used.copy(), options.copy())
                new_state = place_and_update_fill(new_state, blank, letter)
                if new_state is None:
                    return None
                new_state = forward_looking_fill(new_state)
                if new_state is not None:
                    new_state = backtrack_fill(new_state)
                    if new_state is not None:
                        return new_state
    return None

def fill():
    state = build()
    print_board(state[0])
    start = time.perf_counter()
    state = generate_data(state)
    end = time.perf_counter()
    print("Finished processing data in %s seconds." % (end - start))
    start = time.perf_counter()
    state = backtrack_fill(state)
    end = time.perf_counter()
    print("Solved in %s seconds." % (end - start))
    return state
      
process_input()
state = fill()
if state is not None:
    print_board(state[0])
else:
    print("None")

# Isabella Zhu, 2, 2023