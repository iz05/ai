import sys, random

HEIGHT = 20
WIDTH = 10
TRIALS = 5
HEURISTIC_SIZE = 8
POPULATION_SIZE = 500
GENERATIONS = 500
NUM_CLONES = 150
TOURNAMENT_SIZE = 20
MUTATION_RATE = 0.1
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
    for row in board:
        print(row)

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

def place_and_update(board, piece, col):
    min_y = HEIGHT
    for i in range(col, col + width(piece)):
        min_y = min(get_largest_blank(board, i) - get_height(piece, i - col), min_y)
    if min_y < 0:
        return (None, None)
    place_piece(board, piece, min_y, col)
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
    value += f * max_well_depth

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

def play_game(strategy):
    board = convert_to_board(" " * 200)
    points = 0
    while True:
        piece = random.choice(LETTERS)
        max_tup = (None, None, None, None)
        for orientation in ORIENTATIONS[piece]: # orientation is a key in TETRIS_PIECES
            for col in range(0, WIDTH - width(orientation) + 1):
                new_board = board.copy()
                new_board, score = place_and_update(board, orientation, col)
                end_game = False
                if new_board == None:
                    end_game = True
                h = heuristic(new_board, strategy, end_game, score)
                tup = (h, score, new_board, end_game)
                if max_tup[0] == None or h > max_tup[0]:
                    max_tup = tup
        if max_tup[3]:
            return points
        points += max_tup[1]
        board = max_tup[2]

def fitness_function(strategy):
    game_scores = []
    for count in range(0, TRIALS):
        game_scores.append(play_game(strategy))
    return sum(game_scores) / len(game_scores)

def make_change(s):
    i = random.randint(0, len(s) - 1)
    return s[ : i] + (s[i] + 2 * random.random() - 1, ) + s[i + 1 : ]

def breed(s1, s2):
    indices = random.sample([i for i in range(0, HEURISTIC_SIZE)], random.randint(1, HEURISTIC_SIZE - 2))
    s = tuple()
    for i in range(0, HEURISTIC_SIZE):
        if i in indices:
            s += (s2[i], )
        else:
            s += (s1[i], )
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
            return tournament[i][0]
    return tournament[-1][0]

def genetic_algorithm():
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
    print("Finished generation 0")    
    generation = list(generation)
    counter = 0
    while(counter < GENERATIONS):
        strategy_count = 0
        generation = sorted(generation, key = lambda x : -1 * x[1])
        print("Best Strategy in generation %s is %s and has score of %s." % (counter, generation[0][0], generation[0][1]))
        print("Average score in generation %s is %s" % (counter, sum([generation[i][1] for i in range(0, len(generation))]) / len(generation)))
        # input()
        new_generation = set()
        for i in range(0, NUM_CLONES):
            new_generation.add(generation[i])
            print("Evaluating strategy number %s --> %s" % (strategy_count, generation[i][1]))
            strategy_count += 1
        while(len(new_generation) < len(generation)):
            tournament_1, tournament_2 = tournaments(generation)
            strategy_1 = get_strategy(tournament_1)
            strategy_2 = get_strategy(tournament_2)
            child = breed(strategy_1, strategy_2)
            f = fitness_function(child)
            print("Evaluating strategy number %s --> %s" % (strategy_count, f))
            strategy_count += 1
            new_generation.add((child, f))
        generation = list(new_generation)
        counter += 1
        print("Finished generation %s" % counter)
    generation = sorted(generation, key = lambda x : -1 * x[1])
    return generation[0]

print(genetic_algorithm())
