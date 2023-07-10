
#Elina Liu
#12/30/21
#problem: takes too long
import sys
from collections import deque
import time

def print_ladder(list): #prints out the ladder
    for i in list:
        print(i)
#_______________________
#read in dictionary_______-_____
start = time.perf_counter()
with open(sys.argv[1]) as g: #python.exe redretry.py words_06_longer.txt puzzles_longer.txt
    
    all_words = [line.strip() for line in g]

database = dict()
for i in all_words:
    for x in range(len(i)):
        key = i[:x] + "_" + i[x+1:]
        if key not in database.keys():
            database[key] = {i}
        else:
            temp = database[key]
            temp.add(i)
            database[key] = temp
end = time.perf_counter()

#print(database)
print("Time to create the data structure was: " + str((end-start)) + " seconds")

#_________________________________
def find_neighbors(word): #sets the list used in neighbors dictionary
    global database
    the_list = []
    for x in range(len(word)):
        key = word[:x] + "_" + word[x+1:]
        neighbors =  database.get(key)
        for i in neighbors:
            if i != word:
                the_list.append(i)
    return the_list
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
        
        for c in find_neighbors(state):
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
            for c in find_neighbors(state):
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
            for c in find_neighbors(state):
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
# print("There are " + str(len(all_words)) + " words in this dictionary.")
b = ""
with open(sys.argv[2]) as f:
    line_list = [line.strip() for line in f]
start = time.perf_counter()
for ind, pairs in enumerate(line_list):
    #pairs ex: abased abases
    print("Line:", ind)
    a, b = pairs.split()
    ladder = Bi_BFS(a, b)
    if ladder == None:
        print("No solution!")
    else:
        print("Length is:", len(ladder))
        print_ladder(ladder)
    print()
end = time.perf_counter()
print("Time to solve all of these puzzles was: " + str((end-start)) + " seconds" )