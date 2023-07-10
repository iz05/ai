import sys, random, re

HEIGHT = 20
WIDTH = 10
TRIALS = 5
HEURISTIC_SIZE = 8
POPULATION_SIZE = 500
GENERATIONS = 500
NUM_CLONES = 20
TOURNAMENT_SIZE = 20
MUTATION_RATE = 0.8
TOURNAMENT_WIN_PROBABILITY = 0.75

TETRIS_PIECES = {
    ("I", 0) : ["####", ],
    ("I", 1) : ["#", "#", "#", "#"],
    ("O", 0) : ["##", "##"],
    ("T", 0) : [" # ", "###"],
    ("T", 1) : ["# ", "##", "# "],
    ("T", 2) : ["###", " # "],
    ("T", 3) : [" #", "##", " #"],
    ("S", 0) : [" ##", "## "],
    ("S", 1) : ["# ", "##", " #"],
    ("Z", 0) : ["## ", " ##"],
    ("Z", 1) : [" #", "##", "# "],
    ("J", 0) : ["#  ", "###"],
    ("J", 1) : ["##", "# ", "# "],
    ("J", 2) : ["###", "  #"],
    ("J", 3) : [" #", " #", "##"],
    ("L", 0) : ["  #", "###"],
    ("L", 1) : ["# ", "# ", "##"],
    ("L", 2) : ["###", "#  "],
    ("L", 3) : ["##", " #", " #"],
}

HEIGHT_VALUES = {
    ("I", 0) : (0, 0, 0, 0),
    ("I", 1) : (0, ),
    ("O", 0) : (0, 0),
    ("T", 0) : (0, 0, 0),
    ("T", 1) : (0, -1),
    ("T", 2) : (-1, 0, -1),
    ("T", 3) : (-1, 0),
    ("S", 0) : (0, 0, -1),
    ("S", 1) : (-1, 0),
    ("Z", 0) : (-1, 0, 0),
    ("Z", 1) : (0, -1),
    ("J", 0) : (0, 0, 0),
    ("J", 1) : (0, -2),
    ("J", 2) : (-1, -1, 0),
    ("J", 3) : (0, 0),
    ("L", 0) : (0, 0, 0),
    ("L", 1) : (0, 0),
    ("L", 2) : (0, -1, -1),
    ("L", 3) : (-2, 0)
}

HEIGHTS = {
    ("I", 0) : 1,
    ("I", 1) : 4,
    ("O", 0) : 2,
    ("T", 0) : 2,
    ("T", 1) : 3,
    ("T", 2) : 2,
    ("T", 3) : 3,
    ("S", 0) : 2,
    ("S", 1) : 3,
    ("Z", 0) : 2,
    ("Z", 1) : 3,
    ("J", 0) : 2,
    ("J", 1) : 3,
    ("J", 2) : 2,
    ("J", 3) : 3,
    ("L", 0) : 2,
    ("L", 1) : 3,
    ("L", 2) : 2,
    ("L", 3) : 3
}

LETTERS = ["I", "O", "T", "S", "Z", "J", "L"]

ORIENTATIONS = {
    "I" : [("I", 0), ("I", 1)],
    "O" : [("O", 0), ],
    "T" : [("T", 0), ("T", 1), ("T", 2), ("T", 3)],
    "S" : [("S", 0), ("S", 1)],
    "Z" : [("Z", 0), ("Z", 1)],
    "J" : [("J", 0), ("J", 1), ("J", 2), ("J", 3)],
    "L" : [("L", 0), ("L", 1), ("L", 2), ("L", 3)]
}

SCORES = {
    0 : 0,
    1 : 40,
    2 : 100,
    3 : 300,
    4 : 1200
}

def print_board(board):
    if board == None:
        print("GAME OVER")
        return
    test = convert_to_string(board)
    print("=======================")
    for count in range(20):
        print(' '.join(list(("|" + test[count * 10: (count + 1) * 10] + "|"))), " ", count)
    print("=======================")
    print()
    print("  0 1 2 3 4 5 6 7 8 9  ")
    print()

def convert_to_board(string):
    board = []
    for i in range(0, len(string), WIDTH):
        board.append(string[i : i + WIDTH])
    return board

def convert_to_string(board):
    string = ""
    for row in board:
        string += row
    return string

def get_largest_blank(board, col):
    space = -1
    for i in range(0, HEIGHT):
        if board[i][col] == " ":
            space = i
        else:
            return space
    return space

def width(piece):
    return len(TETRIS_PIECES[piece][0])

def height(piece):
    return len(TETRIS_PIECES[piece])

def get_height(piece, col):
    for i in range(height(piece) - 1, -1, -1):
        if TETRIS_PIECES[piece][i][col] == "#":
            return i
    return 0

def place_piece(board, piece, y, x):
    for b in range(0, height(piece)):
        for a in range(0, width(piece)):
            if TETRIS_PIECES[piece][b][a] == "#":
                board[y + b] = board[y + b][ : x + a] + "#" + board[y + b][x + a + 1 : ]

def remove_full_rows(board):
    remove_rows = []
    for i in range(0, HEIGHT):
        if board[i] == "#" * WIDTH:
            remove_rows.append(i)
    new_board = [" " * WIDTH, ] * len(remove_rows)
    for i in range(0, HEIGHT):
        if i not in remove_rows:
            new_board += [board[i], ]
    return (new_board, len(remove_rows))

def place_and_update(board, piece, col, bottom):
    if HEIGHT - bottom - HEIGHTS[piece] < 0:
        return (None, None)
    place_piece(board, piece, HEIGHT - bottom - HEIGHTS[piece], col)
    board, num_of_rows = remove_full_rows(board)
    score = 0
    if num_of_rows > 4:
        score = SCORES[4]
    else:
        score = SCORES[num_of_rows]
    return (board, score)

def heuristic(board, strategy, end_game, score):
    if end_game:
        return -10000000
    value = 0
    a, b, c, d, e, f, g, h = strategy
    
    # pile height
    highest_pile = 0
    for c in range(0, WIDTH):
        for r in range(0, HEIGHT):
            if board[r][c] == "#":
                highest_pile = max(highest_pile, HEIGHT - r)
                break
    value += a * highest_pile

    # holes
    hole_count = 0
    for r in range(1, HEIGHT):
        for c in range(0, WIDTH):
            if board[r][c] == " " and board[r - 1][c] == "#":
                hole_count += 1
    value += b * hole_count

    # removed lines (score)
    value += c * score

    # altitude difference
    min_occupied = HEIGHT
    for r in range(0, HEIGHT):
        for c in range(1, WIDTH):
            if board[r][c] == "#":
                min_occupied = min(min_occupied, r)
                break
    max_reachable = -1
    for c in range(0, WIDTH):
        for r in range(0, HEIGHT):
            if board[r][c] == "#":
                max_reachable = max(max_reachable, r - 1)
    value += d * (max_reachable - min_occupied)

    # maximum well depth
    max_well_depth = 0
    for c in range(0, WIDTH):
        count = 0
        flag = False
        for r in range(0, HEIGHT):
            if board[r][c] == "#":
                max_well_depth = max(count, max_well_depth)
                break
            elif flag or ((c == 0 or board[r][c - 1] == "#") and (c == WIDTH - 1 or board[r][c + 1] == "#")):
                count += 1
                flag = True
    value += e * max_well_depth

    # sum of all wells
    sum_of_wells = 0
    for c in range(0, WIDTH):
        count = 0
        flag = False
        for r in range(0, HEIGHT):
            if board[r][c] == "#":
                sum_of_wells += count
                break
            elif flag or ((c == 0 or board[r][c - 1] == "#") and (c == WIDTH - 1 or board[r][c + 1] == "#")):
                count += 1
                flag = True
    value += f * sum_of_wells

    # blocks
    block_count = 0
    for c in range(0, WIDTH):
        for r in range(0, HEIGHT):
            if board[r][c] == "#":
                block_count += 1
    value += g * block_count

    # weighted blocks
    weighted_block_count = 0
    for c in range(0, WIDTH):
        for r in range(0, HEIGHT):
            if board[r][c] == "#":
                weighted_block_count += HEIGHT - r
    value += h * weighted_block_count

    return value

def play_game(strategy, bool):
    board = convert_to_board(" " * 200)
    points = 0
    while True:
        piece = random.choice(LETTERS)
        max_tup = (-1, -1, -1, -1)
        l = []

        for i in range(0, WIDTH):
            l.append(HEIGHT - 1 - get_largest_blank(board, i))

        for orientation in ORIENTATIONS[piece]: # orientation is a key in TETRIS_PIECES
            for col in range(0, WIDTH - width(orientation) + 1):
                new_board = board.copy()
                heights = []
                for i in range(0, width(orientation)):
                    heights.append(HEIGHT_VALUES[orientation][i] + l[col + i])
                bottom = max(heights)
                new_board, score = place_and_update(new_board, orientation, col, bottom)
                end_game = False
                if new_board == None:
                    end_game = True
                h = heuristic(new_board, strategy, end_game, score)
                tup = (h, score, new_board, end_game)
                if max_tup[0] == -1 or h > max_tup[0]:
                    max_tup = tup
        
        if bool:
            st = convert_to_string(board)
            print("=======================")
            for count in range(20):
                print(' '.join(list(("|" + st[count * 10: (count + 1) * 10] + "|"))), " ", count)
            print("=======================")
            print()
            print("  0 1 2 3 4 5 6 7 8 9  ")
            print()

        if max_tup[3]:
            return points

        points += max_tup[1]
        board = max_tup[2]

def fitness_function(strategy):
    game_scores = []
    for count in range(0, TRIALS):
        game_scores.append(play_game(strategy, False))
    return sum(game_scores) / len(game_scores)

def make_change(s):
    i = random.randint(0, len(s) - 1)
    return s[ : i] + (s[i] + 2 * random.random() - 1, ) + s[i + 1 : ]

def breed(s1, s2):
    s = tuple()
    for i in range(0, HEURISTIC_SIZE):
        if random.random() < 0.5:
            s = s + (s1[i], )
        else:
            s = s + (s2[i], )
    if random.random() < MUTATION_RATE:
        s = make_change(s)
    return s

def tournaments(generation):
    g = generation.copy()
    tournament_1 = random.sample(g, TOURNAMENT_SIZE)
    for item in tournament_1:
        g.remove(item)
    tournament_2 = random.sample(g, TOURNAMENT_SIZE)
    tournament_1 = sorted(list(tournament_1), key = lambda x : -1 * x[1])
    tournament_2 = sorted(list(tournament_2), key = lambda x : -1 * x[1])
    return (tournament_1, tournament_2)

def get_strategy(tournament):
    i = 0
    while(i < len(tournament)):
        prob = random.random()
        if prob < TOURNAMENT_WIN_PROBABILITY:
            return tournament[i]
    return tournament[-1]

def write_generation(generation, filename):
    f = open(filename, "w")
    count = 0
    for g in generation:
        f.write("Strategy %s: %s has score %s.\n" % (count, g[0], g[1]))
        count += 1
    f.close()

def read_generation(filename):
    global GENERATIONS
    generation = []
    lines = open(filename, 'r').readlines()
    for line in lines:
        left = line.index("(")
        right = line.index(")")
        var = line[left + 1 : right]
        l = var.split(", ")
        for i in range(0, len(l)):
            l[i] = float(l[i])
        tup = tuple(l)
        ind = line.rindex(" ")
        score = float(line[ind + 1 : -2])
        generation.append((tup, score))
    GENERATIONS = len(lines)
    return generation

def generate_initial_population():
    generation = set()
    count = 0
    while(len(generation) < POPULATION_SIZE):
        strategy = []
        for i in range(0, HEURISTIC_SIZE):
            strategy.append(2 * random.random() - 1)
        strategy = tuple(strategy)
        f = fitness_function(strategy)
        generation.add((strategy, f))
        print("Evaluating strategy number %s --> %s" % (count, f))
        count += 1
    generation = list(generation)
    return generation

def genetic_algorithm():
    user_input = input("Start a new genetic process (N) or load a saved genetic process (S) ")
    print()
    generation = None
    while user_input != "S" and user_input != "N":
        user_input = input("Error in input. Please enter 'N' for a new generation or 'S' for a saved generation. ")
        print()
    if user_input == "N":
        generation = generate_initial_population()
    elif user_input == "S":
        file_name = input("Please enter the file name of the generation. Make sure it follows the same format as generation.txt ")
        generation = read_generation(file_name)
        print("Strategy loaded.")
    print()
    counter = 0
    generation = sorted(generation, key = lambda x : -1 * x[1])
    print("Best Strategy in generation %s is %s and has score of %s." % (counter, generation[0][0], generation[0][1]))
    print("Average score in generation %s is %s" % (counter, sum([generation[i][1] for i in range(0, len(generation))]) / len(generation)))
    print()

    while(counter < GENERATIONS):
        user_input = input("Watch a game (W) or save the current generation (S) or continue (C) ")
        print()
        while user_input != "S" and user_input != "C":
            if user_input == "W":
                score = play_game(generation[0][0], True)
                print("Best strategy scored %s points." % score)
                print()
                user_input = input("Watch a game (W) or save the current generation (S) or continue (C) ")
                print()
            else:
                user_input = input("Error in input. Please enter 'W' to watch a game, 'S' to save the current generation, or 'C' to continue. ")
                print()

        if user_input == "S":
            filename = input("Please enter the name of the file you wish to save the current generation to. ")
            write_generation(generation, filename)
            break

        strategy_count = 0
        new_generation = set()
        for i in range(0, NUM_CLONES):
            new_generation.add(generation[i])
            print("Evaluating strategy number %s --> %s" % (strategy_count, generation[i][1]))
            strategy_count += 1
        while(len(new_generation) < len(generation)):
            tournament_1, tournament_2 = tournaments(generation)
            strategy_1 = get_strategy(tournament_1)
            strategy_2 = get_strategy(tournament_2)
            child = breed(strategy_1[0], strategy_2[0])
            f = fitness_function(child)
            print("Evaluating strategy number %s --> %s" % (strategy_count, f))
            strategy_count += 1
            new_generation.add((child, f))
        generation = list(new_generation)
        counter += 1
        generation = sorted(generation, key = lambda x : -1 * x[1])
        print()
        print("Best Strategy in generation %s is %s and has score of %s." % (counter, generation[0][0], generation[0][1]))
        print("Average score in generation %s is %s" % (counter, sum([generation[i][1] for i in range(0, len(generation))]) / len(generation)))
        print()

genetic_algorithm()