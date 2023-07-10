import sys

def display_dict(dfa, alphabet):
    row0 = "*\t\t"
    for char in alphabet:
        row0 += char + "\t\t"
    print(row0)
    for state in dfa:
        row = ""
        state_dict = dfa[state]
        row += str(state) + "\t\t"
        for char in alphabet:
            if char in state_dict:
                row += str(state_dict[char]) + "\t\t"
            else:
                row += "_\t\t"
        print(row)

def emulate(dfa, final_states, puzzle):
    state = 0
    for char in puzzle:
        if char in dfa[state]:
            state = dfa[state][char]
        else:
            return False
    if state in final_states:
        return True
    return False

def part1():
    # processing data
    text_file = open(sys.argv[1], "r")
    text = text_file.read()
    text_file.close()
    lines = text.split("\n\n")

    dfa = {}
    num_of_states = 0
    final_states = []
    alphabet = ""

    start = lines[0].split("\n")
    alphabet = start[0]
    num_of_states = int(start[1])
    states = start[2].split(" ")
    for state in states:
        final_states.append(int(state))

    for index in range(0, num_of_states):
        cur_dict = {}
        data = lines[index + 1].split("\n")
        for i in range(1, len(data)):
            cur_dict[data[i][0]] = int(data[i][2])
        cur_state = int(data[0])
        dfa[cur_state] = cur_dict
    display_dict(dfa, alphabet)
    print("Final nodes: " + str(final_states))
    puzzles = open(sys.argv[2], "r").read().split("\n")
    num_of_spaces = {
        True: 2,
        False: 1
    }

    for puzzle in puzzles:
        result = emulate(dfa, final_states, puzzle)
        print(str(result) + " " * num_of_spaces[result] + puzzle)

def part2():
    num = int(sys.argv[1])

    puzzles = open(sys.argv[2], "r").read().split("\n")
    num_of_spaces = {
        True: 2,
        False: 1
    }

    dfa = {}
    final_states = []
    alphabet = ""
    if num == 1:
        dfa = {
            0 : {
                "a" : 1
            },
            1 : {
                "a" : 2
            },
            2 : {
                "b" : 3
            },
            3 : {}
        }
        final_states = [3, ]
        alphabet = "ab"
    elif num == 2:
        dfa = {
            0 : {
                "0" : 0,
                "1" : 1,
                "2" : 0
            },
            1 : {
                "0" : 0,
                "1" : 1,
                "2" : 0
            },
        }
        final_states = [1, ]
        alphabet = "012"
    elif num == 3:
        dfa = {
            0 : {
                "a" : 0,
                "b" : 1,
                "c" : 0
            },
            1 : {
                "a" : 1,
                "b" : 1,
                "c" : 1
            },
        }
        final_states = [1, ]
        alphabet = "abc"
    elif num == 4:
        dfa = {
            0 : {
                "0" : 1,
                "1" : 0,
            },
            1 : {
                "0" : 0,
                "1" : 1,
            },
        }
        final_states = [0, ]
        alphabet = "01"
    elif num == 5:
        dfa = {
            0 : {
                "0" : 2,
                "1" : 1,
            },
            1 : {
                "0" : 3,
                "1" : 0,
            },
            2 : {
                "0" : 0,
                "1" : 3,
            },
            3 : {
                "0" : 1,
                "1" : 2,
            },
        }
        final_states = [0, ]
        alphabet = "01"
    elif num == 6:
        dfa = {
            0 : {
                "a" : 1,
                "b" : 0,
                "c" : 0
            },
            1 : {
                "a" : 1,
                "b" : 2,
                "c" : 0
            },
            2 : {
                "a" : 1,
                "b" : 0,
                "c" : 3
            },
            3 : {}
        }
        final_states = [0, 1, 2]
        alphabet = "abc"
    elif num == 7:
        dfa = {
            0 : {
                "0" : 0,
                "1" : 1,
            },
            1 : {
                "0" : 2,
                "1" : 1,
            },
            2 : {
                "0" : 2,
                "1" : 3
            },
            3 : {
                "0" : 2,
                "1" : 4
            },
            4 : {
                "0" : 4,
                "1" : 4
            }
        }
        final_states = [4, ]
        alphabet = "01"
    else:
        print("Out of bounds")
    
    display_dict(dfa, alphabet)
    print("Final nodes: " + str(final_states))

    for puzzle in puzzles:
        result = emulate(dfa, final_states, puzzle)
        print(str(result) + " " * num_of_spaces[result] + puzzle)

try:
    num = int(sys.argv[1])
    part2()
except ValueError:
    part1()