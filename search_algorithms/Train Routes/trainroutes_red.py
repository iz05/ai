#1 Liu Elina
import sys
from math import pi , acos , sin , cos
from collections import deque
from heapq import heapify, heappush, heappop
import time
import tkinter as tk
import math
from threading import Event
with open("rrEdges.txt") as f: #read the id -- ids
      info_list = [line.strip() for line in f]
#great circle distance from distanceDemo.py
def calcd(node1, node2): #@param: float tuples (lat, long)
   # y1 = lat1, x1 = long1
   # y2 = lat2, x2 = long2
   # all assumed to be in decimal degrees
   if node1 == node2:
      return 0
   y1, x1 = node1
   y2, x2 = node2

   R   = 3958.76 # miles = 6371 km
   y1 *= pi/180.0
   x1 *= pi/180.0
   y2 *= pi/180.0
   x2 *= pi/180.0

   # approximate great circle distance with law of cosines
   return acos( sin(y1)*sin(y2) + cos(y1)*cos(y2)*cos(x2-x1) ) * R
def make_coords(): #returns dictionary of coords (id: (x,y))
   coord_dict = dict()
   with open("rrNodes.txt") as f: #
      info_list = [line.strip() for line in f] #info is list of "id lat long"
   for i in info_list:
      x = i.split()
      coord_dict[x[0]] = (float(x[1]),float(x[2]))
   return coord_dict

def make_names(): #dict = name: id for major stops only
   names_dict = dict()
   with open("rrNodeCity.txt") as f:
      info_list = [line.strip() for line in f]
   for i in info_list:
      x = i.split(" ", 1)
      names_dict[x[1]] = x[0]
   return names_dict
def make_edges(): # id: [(id_a, weight), (id_b, weight), (etc)]
   edges_dict = dict()
   global info_list
   for i in info_list: # a b 
      x = i.split()
      
      if x[0] in edges_dict:
         edges_dict[x[0]].append((x[1], calcd(coords[x[0]], coords[x[1]]))) #NEEDS TO CHANGE TO ADD WEIGHT
      else:
         edges_dict[x[0]] = [(x[1], calcd(coords[x[0]], coords[x[1]]))] # = [(b, calcd(a,b))]
      if x[1] in edges_dict:
         edges_dict[x[1]].append((x[0], calcd(coords[x[1]], coords[x[0]]))) #NEEDS TO CHANGE TO ADD WEIGHT
      else:
         edges_dict[x[1]] = [(x[0], calcd(coords[x[1]], coords[x[0]]))] # = [(b, calcd(a,b))]
   return edges_dict

def find_goal(id): #not necessary tbh
   return(names[jail])
def get_children(id): #input is string, returns b_list one move away from state
   children = edges[id]
   toRet = []
   for x, y in children:
      toRet.append(x)
   return toRet
def goal_test(id): #returns true if board matches find_goal
    return(id == names[jail])
def a_star(id):
    closed = set()
    fringe = []
    heapify(fringe)
    path = list()
    path.append(id)
    startnode = (calcd(coords[id], coords[names[jail]]), id, 0) #heuristic, state, depth
    heappush(fringe, (startnode, path))
   # times = 0 #a counter for animation
    while len(fringe) > 0:
        stuff, path = heappop(fringe)
        f, state, depth = stuff
        if goal_test(state):
            return depth, path
        if state not in closed:
            closed.add(state)
            for c in get_children(state):
                if c not in closed:
                    estimate = calcd(coords[c], coords[names[jail]])
                    new_path = path.copy()
                    new_path.append(c)
                    heappush(fringe, ((depth + weight(c, state) + estimate, c, depth+weight(c, state)), new_path))
                 #   times += 1
                #    if times%10 == 0:
                    make_red(root, canvas, (state, c))
    return None
def weight(a, b): #weight of edge[a] to b
   children = edges[a] #a list
   for x, y in children:
      if x == b:
         return y
def dij(id): #modified a_star
   closed = set()
   fringe = []
   heapify(fringe)
   path = list()
   path.append(id)
   startnode = (0, id) #depth, state
   heappush(fringe, (startnode, path))
   while len(fringe) > 0:
      stuff, path = heappop(fringe)
      depth, state = stuff
      if goal_test(state):
         return depth, path
      if state not in closed:
         closed.add(state)
         for c in get_children(state):
               if c not in closed:
                  new_path = path.copy()
                  new_path.append(c)
                  heappush(fringe, ((depth+weight(c, state), c), new_path)) #depth, state

   return None

#__________________________
tracks = dict() #key: (node1, node2)
def find_min_max_coords():
    with open("rrNodes.txt") as f: #read the id -- ids
      aaa = [line.strip() for line in f]
    maxlat = -math.inf
    maxlong = -math.inf
    minlat = math.inf
    minlong = math.inf
    for i in aaa:
        id, lat, long = i.split()
        lat = float(lat)
        long = float(long)
        if lat < minlat:
            minlat = lat
        if lat > maxlat:
            maxlat = lat
        if long <minlong:
            minlong= long
        if long > maxlong:
            maxlong = long
    return (maxlat, maxlong, minlat, minlong)
maxlat, maxlong, minlat, minlong = find_min_max_coords() #integers
def convert_latlong(lat, long): #passed as strings, sent back as integers
    global maxlat, maxlong, minlat, minlong
    lat = float(lat)
    long = float(long)
    #x = abs((long - minlong) * 800 / (maxlong - minlong))
    #y = abs(maxlat - (lat - minlat) * 800 / (maxlat - minlat))
    x = (long - minlong) *500.0 / (maxlong - minlong)
    y = (lat - minlat)*400.0 / (maxlat-minlat)
    return x, 500-y 
def create_tracks(c, coords): #dictionary, id:[(neighbor_id, distanceaway)]
    #sets up the edges as black lines
    global info_list
    global tracks
    for it in info_list:
       # print(it)
        node1, node2 = it.split()
        lat1, long1 = coords.get(node1)
     #   print(lat1, long1)
        x1, y1 = convert_latlong(lat1, long1)
        lat2, long2 = coords.get(node2)
        x2, y2= convert_latlong(lat2, long2)
        tracks[(node1, node2)] = c.create_line(x1, y1, x2, y2)
def make_red(r, c, id): #red line at (n1, n2)key, asattar
	line = tracks.get(id)
	c.itemconfig(line, fill="red") #changes color of one line to red
	r.update() #update frame
		#time.sleep(0.1)
def make_blue(r, c, id): #blue line, dhjistsra
	line = tracks.get(id)
	c.itemconfig(line, fill="blue") #changes color of one line to red
	r.update() #update frame
def make_green(r, c, id): #final path
	line = tracks.get(id)
	c.itemconfig(line, fill="green") #changes color of one line to red
	r.update() #update frame
def draw_final(path):
    for i in range(len(path)-1):
        make_green(root, canvas, (path[i], path[i+1]))
        
##main---------------------------------------------
coords = make_coords() #a dictionary, id: (lat, long)
names = make_names() #dictionary, name:id
start = time.perf_counter()
edges = make_edges() #dictionary, id:[(neighbor_id, distanceaway)]

end = time.perf_counter()
print("Time to create data structure: " + str(end-start) + " seconds")

go = sys.argv[1] #type python.exe trainroutes_red.py Albuquerque Atlanta
jail = sys.argv[2] #ending place
goal = names[jail]

root = tk.Tk() #creates the frame

canvas = tk.Canvas(root, height=800, width=500, bg='white') #creates a canvas widget, which can be used for drawing lines and shapes
create_tracks(canvas, coords)
canvas.pack(expand=True)

s = str(go) + " to " + str(jail) + " with Dijkstra: " 
start = time.perf_counter()
answer, path = dij(names[go])
draw_final(path)
s += str(answer) + " in " 
end = time.perf_counter()
s += str(end-start) + " seconds."
print(s)

Event().wait(5) 

# #a*! comment this out to see djistra only______________
s = str(go) + " to " + str(jail) + " with A*: " 
start = time.perf_counter()
answer, path = a_star(names[go])
draw_final(path)
s += str(answer) + " in " 
end = time.perf_counter()
s += str(end-start) + " seconds."
print(s)
#________________________________________________________

root.mainloop()

