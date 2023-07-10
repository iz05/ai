import sys; args = sys.argv[1:]
myLines = open(args[0], 'r').read().splitlines()

import time, math, random, re

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
h_neighbors = {}
v_neighbors = {}

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
    return spaces # returns all squares with "."

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

def generate_data(state): # fills horizontal, vertical, h_neighbors, v_neighbors, and generates state to be filled given input state from build()
    global horizontal, vertical, h_neighbors, v_neighbors, words
    puzzle, block_squares, blank_squares = state
    positions = set()
    options = {}
    words_used = set()
    word_bank = {}

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

        if puzzle[row][col] != "-":
            positions.add(space)
    
    # figure out if there are any words completely filled
    for blank in blank_squares:
        row, col = blank
        # check if it is the start of a horizontal word
        if (row, col - 1) not in blank_squares:
            i = 0
            word = ""
            while (row, col + i) in blank_squares:
                word = word + puzzle[row][col + i]
                if puzzle[row][col + i] == "-":
                    break
                i += 1
            if word[-1] != "-":
                words_used.add(word)
        # check if its the start of a vertical word
        if (row - 1, col) not in blank_squares:
            i = 0
            word = ""
            while(row + i, col) in blank_squares:
                word = word + puzzle[row + i][col]
                if puzzle[row + i][col] == "-":
                    break
                i += 1
            if word[-1] != "-":
                words_used.add(word)
    
    words = words.difference(words_used)

    # calculate options
    for blank in blank_squares:
        row, col = blank
        if puzzle[row][col] == "-":
            temp = set()
            for word in words:
                flag = True
                if len(word) != horizontal[blank][0]:
                    flag = False
                if flag:
                    for neighbor in h_neighbors[blank]:
                        if flag:
                            row2, col2 = neighbor
                            if puzzle[row2][col2] != "-":
                                letter = puzzle[row2][col2]
                                length, position = horizontal[neighbor]
                                if letter != word[position]:
                                    flag = False
                if flag:
                    temp.add(word[horizontal[blank][1]])

            temp2 = set()
            for word in words:
                flag = True
                if len(word) != vertical[blank][0]:
                    flag = False
                if flag:
                    for neighbor in v_neighbors[blank]:
                        if flag:
                            row2, col2 = neighbor
                            if puzzle[row2][col2] != "-":
                                letter = puzzle[row2][col2]
                                length, position = vertical[neighbor]
                                if letter != word[position]:
                                    flag = False
                if flag:
                    temp2.add(word[vertical[blank][1]])
            temp = temp.intersection(temp2)
            options[blank] = temp
    return (puzzle, positions, options, words_used, words)

def get_word(state, space, orientation):
    pass

def get_space_fill(state):
    options = state[2]
    min_space = None
    min_num = 27
    for space in options:
        if len(options[space]) == 0:
            return None
        elif len(options[space]) < min_num:
            min_space = space
            min_num = len(options[space])
    return min_space

def place_and_update_fill(state, space, letter):
    puzzle, positions, options, words_used, word_bank = state
    row, col = space

    # update puzzle
    puzzle[row] = puzzle[row][ : col] + letter + puzzle[row][col + 1 : ]

    # update positions
    positions.add((row, col))

    # update options
    del options[space]
    for blank in options:
        row, col = blank
        if puzzle[row][col] == "-":
            temp = set()
            for word in words:
                flag = True
                if len(word) != horizontal[blank][0]:
                    flag = False
                if flag:
                    for neighbor in h_neighbors[blank]:
                        if flag:
                            row2, col2 = neighbor
                            if puzzle[row2][col2] != "-":
                                letter = puzzle[row2][col2]
                                length, position = horizontal[neighbor]
                                if letter != word[position]:
                                    flag = False
                if flag:
                    temp.add(word[horizontal[blank][1]])

            temp2 = set()
            for word in words:
                flag = True
                if len(word) != vertical[blank][0]:
                    flag = False
                if flag:
                    for neighbor in v_neighbors[blank]:
                        if flag:
                            row2, col2 = neighbor
                            if puzzle[row2][col2] != "-":
                                letter = puzzle[row2][col2]
                                length, position = vertical[neighbor]
                                if letter != word[position]:
                                    flag = False
                if flag:
                    temp2.add(word[vertical[blank][1]])
            temp = temp.intersection(temp2)
            options[blank] = temp

    # update words_used
    row, col = space
    flag = True # check for horizontal word
    for sp in h_neighbors[space]:
        r, c = sp
        if puzzle[r][c] == "-":
            flag = False
            break
    if flag:
        word = ""
        i = 0
        while col + i >= 0 and puzzle[row][col + i] != "#":
            word = puzzle[row][col + i] + word
            i -= 1
        i = 1
        while col + i < width and puzzle[row][col + i] != "#":
            word = word + puzzle[row][col + i]
            i += 1
        if word in word_bank:
            words_used.add(word)
            word_bank.remove(word)
        else:
            return None
    flag = True # check for vertical word
    for sp in v_neighbors[space]:
        r, c = sp
        if puzzle[r][c] == "-":
            flag = False
            break
    if flag:
        word = ""
        i = 0
        while row + i >= 0 and puzzle[row + i][col] != "#":
            word = puzzle[row + i][col] + word
            i -= 1
        i = 1
        while row + i < height and puzzle[row + i][col] != "#":
            word = word + puzzle[row + i][col]
            i += 1
        if word in word_bank:
            words_used.add(word)
            word_bank.remove(word)
        else:
            return None

    return state

def copy(state):
    puzzle, positions, options, words_used, word_bank = state
    puzzle2 = puzzle.copy()
    positions2 = positions.copy()
    options2 = {}
    for space in options:
        options2[space] = options[space].copy()
    words_used2 = words_used.copy()
    word_bank2 = word_bank.copy()
    return (puzzle2, positions2, options2, words_used2, word_bank2)

def backtrack_fill(state):
    puzzle, positions, options, words_used, word_bank = state
    if len(state[1]) == blanks:
        return state
    space = get_space_fill(state)
    if space == None:
        return None
    for letter in options[space]:
        temp = copy(state)
        temp = place_and_update_fill(temp, space, letter)
        if temp is not None:
            temp = backtrack_fill(temp)
            if temp is not None:
                return temp

def fill():
    state = build()
    state = generate_data(state)
    state = backtrack_fill(state)
    return state
      
process_input()
state = fill()
if state is not None:
    print_board(state[0])
else:
    print("None")


# Isabella Zhu, 2, 2023