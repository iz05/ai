from math import log
from random import randint, random
import sys

# global variables
POPULATION_SIZE = 500
NUM_CLONES = 1
TOURNAMENT_SIZE = 20
TOURNAMENT_WIN_PROBABILITY = 0.75
CROSSOVER_LOCATIONS = 5
MUTATION_RATE = 0.8

def index(char): # returns the index of uppercase char in alphabet
    return ord(char) - 65

def encode(cipher, message):
    m = ""
    message = message.upper()
    for char in message:
        if char in cipher:
            m += cipher[index(char)]
        else:
            m += char
    return m

def decode(cipher, message):
    m = ""
    for char in message:
        if char in cipher:
            ind = cipher.find(char)
            m += chr(ind + 65)
        else:
            m += char
    return m

def fitness(n, text, cipher):
    global ngrams
    text = text.upper()
    message = decode(cipher, text)
    s = 0
    for i in range(0, len(message) - n + 1):
        gram = message[i : i + n]
        if gram in ngrams:
            s += log(ngrams[gram], 2)
    return s

def random_permutation():
    letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    p = ""
    for i in range(25, -1, -1):
        num = randint(0, i)
        p += letters[num]
        del letters[num]
    return p

def make_change(cipher):
    i = randint(0, 25)
    j = randint(0, 25)
    while i == j:
        j = randint(0, 25)
    a = min(i, j)
    b = max(i, j)
    return cipher[ : a] + cipher[b] + cipher[a + 1 : b] + cipher[a] + cipher[b + 1 :]

def hill_climbing(message):
    cipher = random_permutation()
    max_score = fitness(4, message, cipher)
    print(decode(cipher, message))
    while(True):
        new_cipher = make_change(cipher)
        new_score = fitness(4, message, new_cipher)
        if new_score > max_score:
            max_score = new_score
            cipher = new_cipher
            print(decode(new_cipher, message))

def tournaments(generation, message):
    g = generation.copy()
    tournament_1 = set()
    tournament_2 = set()
    for i in range(0, TOURNAMENT_SIZE):
        index = randint(0, len(g) - 1)
        tournament_1.add(g[index])
        del g[index]
    for i in range(0, TOURNAMENT_SIZE):
        index = randint(0, len(g) - 1)
        tournament_2.add(g[index])
        del g[index]
    tournament_1 = sorted(list(tournament_1), key = lambda x : -1 * x[1])
    tournament_2 = sorted(list(tournament_2), key = lambda x : -1 * x[1])
    return (tournament_1, tournament_2)

def get_strategy(tournament):
    i = 0
    while(i < len(tournament)):
        prob = random()
        if prob < TOURNAMENT_WIN_PROBABILITY:
            return tournament[i][0]
    return tournament[-1][0]

def breed(s1, s2):
    locations = set()
    while(len(locations) < CROSSOVER_LOCATIONS):
        locations.add(randint(0, 25))
    child = [None, ] * 26
    child_letters = set()
    for l in locations:
        child[l] = s1[l]
        child_letters.add(s1[l])
    index_child = 0
    index_parent = 0
    while(index_child < 26):
        if child[index_child] != None:
            index_child += 1
        elif s2[index_parent] in child_letters:
            index_parent += 1
        else:
            child[index_child] = s2[index_parent]
            index_child += 1
            index_parent += 1
    output = ""
    for char in child:
        output += char
    if random() < MUTATION_RATE:
        output = make_change(output)
    return output

def genetic_algorithm(message):
    generation = set()
    while(len(generation) < POPULATION_SIZE):
        perm = random_permutation()
        generation.add((perm, fitness(4, message, perm)))
    generation = list(generation)
    counter = 0
    while(True):
        generation = sorted(generation, key = lambda x : -1 * x[1])
        print("Generation %s: %s" % (counter, decode(generation[0][0], message)))
        if counter >= 500:
            return decode(generation[0][0], message)
        new_generation = set()
        for i in range(0, NUM_CLONES):
            new_generation.add(generation[i])
        while(len(new_generation) < len(generation)):
            tournament_1, tournament_2 = tournaments(generation, message)
            strategy_1 = get_strategy(tournament_1)
            strategy_2 = get_strategy(tournament_2)
            child = breed(strategy_1, strategy_2)
            new_generation.add((child, fitness(4, message, child)))
        generation = list(new_generation)
        counter += 1

# make a dictionary of ngrams
ngrams = {}
lines = open("ngrams.txt", 'r').read().splitlines()
for line in lines:
    a = line.split(" ")
    ngrams[a[0]] = int(a[1])
    
genetic_algorithm(sys.argv[1])
