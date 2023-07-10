
#Elina Liu
#12/30/21
#removable + addable
import sys
from collections import deque
import time
import random

def print_ladder(list): #prints out the ladder
    for i in list:
        print(i)

#_______________________
#read in dictionary_______-_____
start = time.perf_counter()
with open("words_all.txt") as g: #python.exe word_ladders_bibfs.py dictionary.txt puzzles_normal.txt
    
    all_words = [line.strip() for line in g]
end = time.perf_counter()
print("Time to create the data structure was: " + str((end-start)) + " seconds")
#_________________________________
def find_neighbors(word, all_words): #sets the list used in neighbors dictionary
    the_list = []
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    for x in range(6): #word length
        for i in range(len(alphabet)): #LOOP THRU ALPHABET
            s = word[0:x] + alphabet[i:i+1] + word[x+1:] #s is a word one letter off from origin word
            if s in all_words:
                if s != word: 
                    the_list.append(s)
            add = word[0:x] + alphabet[i:i+1] + word[x:]
            if add in all_words:
                if add != word: 
                    the_list.append(add)
        sub = word[0:x] + word[x+1:] #cuts out index x
        if sub in all_words:
            if sub != word: 
                the_list.append(sub)
        

    
    return the_list

def get_children(word): #input is string, returns b_list one move away from state
    return find_neighbors(word, all_words)

def goal_test(word): #returns true if word is the end word
    global b
    return(word == b) 
def BFS(start, stop):
    
    fringe = deque()                #new Queue .append(), .popleft()
    visited = set()                 #new Set
    fringe.append((start, []))      #word, ladder
    visited.add(start)
   
    while len(fringe) > 0:
        state, path = fringe.popleft()
    
        if state == stop :             
            path.append(state)
            return path                
        
        for c in find_neighbors(state, all_words):
            if c not in visited:
                new_path = path.copy()
                new_path.append(state)
                fringe.append((c, new_path))
                visited.add(c)   
    
    return None

# def BFS(start):
#     fringe = deque() #new Queue .append(), .popleft()
#     visited = set() #new Set
#     fringe.append((start, [])) #word, ladder
#     visited.add(start)
#     while len(fringe) > 0:
#         v = fringe.popleft()
#         state, path = v
#         if goal_test(state): 
#             path.append(b)
#             return path #list thats the ladder
#         for c in get_children(state):
#             if c not in visited:
#                 new_path = path.copy()
#                 new_path.append(state)
#                 fringe.append((c, new_path))
#                 visited.add(c)   
#     return None
def Bi_BFS(source, goal): #way faster than BFS
    sourcefringe = deque() #new Queue .append(), .popleft()
    sourcevisited = set() #new Set
    goalfringe = deque()
    goalvisited = set()
    sourcefringe.append((source, []))
    sourcevisited.add(source)
    goalfringe.append((goal, []))
    goalvisited.add(goal)
    while len(sourcefringe) > 0 and len(goalfringe) >0:

        stemp = sourcefringe.copy()
        sourcefringe = deque()
        while len(stemp) > 0:
            s = stemp.popleft()
            state, path = s
            goalstates = [x[0] for x in goalfringe]
            goalpaths = [x[1] for x in goalfringe]
            if state in goalstates: 
               # print("the state is: ", state)
                final_path = path.copy()
                final_path.append(state)
                other_path = goalpaths[goalstates.index(state)]
                other_path.reverse()
                for i in other_path:
                    final_path.append(i)
                return final_path
            for c in get_children(state):
                if c not in sourcevisited:
                    new_path = path.copy()
                    new_path.append(state)
                    sourcefringe.append((c, new_path))
                    sourcevisited.add(c)

        gtemp = goalfringe.copy()
        goalfringe = deque()
        while len(gtemp) > 0:
            s = gtemp.popleft()
            state, path = s
            sourcestates = [x[0] for x in sourcefringe]
            sourcepaths = [x[1] for x in sourcefringe]
            if state in sourcestates: 
               # print("the state is: ", state)
                other_path = sourcepaths[sourcestates.index(state)]
                other_path.append(state)
                path.reverse()
                for i in path:
                    other_path.append(i)
                return other_path
            for c in get_children(state):
                if c not in goalvisited:
                    new_path = path.copy()
                    new_path.append(state)
                    goalfringe.append((c, new_path))
                    goalvisited.add(c)
        
    return None
#___________________________________
#main_______________________________
#___________________________________
#global is b
#print("There are " + str(len(all_words)) + " words in this dictionary.")
b = ""
with open("puzzles_all.txt") as f:
    line_list = [line.strip() for line in f]
start = time.perf_counter()
for ind, pairs in enumerate(line_list):
    #pairs ex: abased abases
    print("Line:", ind)
    a, b = pairs.split()
    ladder = BFS(a, b)
    if ladder == None:
        print("No solution!")
    else:
        print("Length is:", len(ladder))
        print_ladder(ladder)
    print()
end = time.perf_counter()
print("Time to solve all of these puzzles was: " + str((end-start)) + " seconds" )
#currently: Time to solve all of these puzzles was: 316.11335249999996 seconds