# playfair cipher decoder using genetic algorithms
# Isabella Zhu
# March 02, 2022

# to make less general, use a key

from math import log
from random import randint, random
import sys

# global variables
POPULATION_SIZE = 500
NUM_CLONES = 1
TOURNAMENT_SIZE = 20
TOURNAMENT_WIN_PROBABILITY = 0.75
CROSSOVER_LOCATIONS = 2
MUTATION_RATE = 0.9
KEY_LENGTH = 5

ALPHABET = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

def complete_alphabet(cipher):
    for char in ALPHABET:
        if char not in cipher:
            cipher += char
    return cipher

def decode(cipher, message):
    message = message.upper()
    cipher = complete_alphabet(cipher)
    code = ""
    a = 0
    b = 1
    while a < len(message):
        while(a < len(message) and not message[a].isalpha()):
            code += message[a]
            a += 1
        
        if a == len(message):
            return code
        
        b = a + 1
        while(b < len(message) and not message[b].isalpha()):
            code += message[b]
            b += 1
        
        if b == len(message):
            message += "X"

        char1 = message[a]
        char2 = message[b]

        ind1 = cipher.index(char1)
        ind2 = cipher.index(char2)
        r1, c1, r2, c2 = ind1 // 5, ind1 % 5, ind2 // 5, ind2 % 5

        if r1 == r2:
            code = code[ : a] + cipher[5 * r1 + ((c1 - 1) % 5)] + code[a : ] + cipher[5 * r2 + ((c2 - 1) % 5)]
        elif c1 == c2:
            code = code[ : a] + cipher[5 * ((r1 - 1) % 5) + c1] + code[a : ] + cipher[5 * ((r2 - 1) % 5) + c2]
        else:
            code = code[ : a] + cipher[5 * r1 + c2] + code[a : ] + cipher[5 * r2 + c1]
        
        a = b + 1
        b = b + 1
    return code

def encode(cipher, message):
    message = message.upper()
    cipher = complete_alphabet(cipher)
    while True:
        index = message.find("J")
        if index == -1:
            break
        message = message[ : index] + "I" + message[index + 1 : ]
    code = ""
    a = 0
    b = 1
    while a < len(message):
        while(a < len(message) and not message[a].isalpha()):
            code += message[a]
            a += 1
        
        if a == len(message):
            return code
        
        b = a + 1
        while(b < len(message) and not message[b].isalpha()):
            code += message[b]
            b += 1
        
        if b == len(message):
            message += "X"

        char1 = message[a]
        char2 = message[b]

        ind1 = cipher.index(char1)
        ind2 = cipher.index(char2)
        r1, c1, r2, c2 = ind1 // 5, ind1 % 5, ind2 // 5, ind2 % 5

        if r1 == r2:
            code = code[ : a] + cipher[5 * r1 + ((c1 + 1) % 5)] + code[a : ] + cipher[5 * r2 + ((c2 + 1) % 5)]
        elif c1 == c2:
            code = code[ : a] + cipher[5 * ((r1 + 1) % 5) + c1] + code[a : ] + cipher[5 * ((r2 + 1) % 5) + c2]
        else:
            code = code[ : a] + cipher[5 * r1 + c2] + code[a : ] + cipher[5 * r2 + c1]
        
        a = b + 1
        b = b + 1
    return code

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
    letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    p = ""
    for i in range(KEY_LENGTH - 1, -1, -1):
        num = randint(0, len(letters) - 1)
        p += letters[num]
        del letters[num]
    return p

def make_change(cipher):
    if KEY_LENGTH == 25:
        for k in range(0, 5):
            i = randint(0, 24)
            j = randint(0, 24)
            while i == j:
                j = randint(0, 24)
            a = min(i, j)
            b = max(i, j)
            cipher = cipher[ : a] + cipher[b] + cipher[a + 1 : b] + cipher[a] + cipher[b + 1 : ]
        return cipher
    i = randint(0, KEY_LENGTH - 1)
    j = randint(0, 24)
    while ALPHABET[j] in cipher:
        j = randint(0, 24)
    return cipher[ : i] + ALPHABET[j] + cipher[i + 1 : ]

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
        locations.add(randint(0, KEY_LENGTH - 1))
    child = [None, ] * KEY_LENGTH
    child_letters = set()
    for l in locations:
        child[l] = s1[l]
        child_letters.add(s1[l])
    index_child = 0
    index_parent = 0
    while(index_child < KEY_LENGTH):
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
        print("Generation %s: cipher %s produces %s" % (counter, generation[0][0], decode(generation[0][0], message)))
        if counter >= 1000:
            return decode(generation[0][0], message)
        new_generation = set()
        for i in range(0, NUM_CLONES):
            new_generation.add(generation[i])
        while(len(new_generation) < POPULATION_SIZE):
            tournament_1, tournament_2 = tournaments(generation, message)
            strategy_1 = get_strategy(tournament_1)
            strategy_2 = get_strategy(tournament_2)
            child = breed(strategy_1, strategy_2)
            new_generation.add((child, fitness(4, message, child)))
        generation = list(new_generation)
        counter += 1

# brute force method

def generate(l, alphabet):
    output = set()
    if l == 1:
        for letter in alphabet:
            output.add(letter)
        return output
    
    for letter in alphabet:
        a = alphabet.copy()
        a.remove(letter)
        keys = generate(l - 1, a)
        for key in keys:
            output.add(key + letter)
    
    return output

def brute_force(code):
    global KEY_LENGTH, ALPHABET
    keys = generate(KEY_LENGTH, set(ALPHABET))
    print("Finished generating")
    max_score = -1
    max_key = "AAAAAAAAAA"
    
    for key in keys:
        score = fitness(4, code, key)
        if score > max_score:
            max_key = key
            max_score = score
    
    print(decode(max_key, code))

# make a dictionary of ngrams
ngrams = {}
lines = open("ngrams.txt", 'r').read().splitlines()
for line in lines:
    a = line.split(" ")
    ngrams[a[0]] = int(a[1])

code = "AOSHFQOAYDIFFTQZPSDTBSETVMQAKI"
print(genetic_algorithm(code))