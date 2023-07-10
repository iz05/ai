# Isabella Zhu

from collections import deque
from heapq import heappush, heappop, heapify
from distanceDemo import calcd
import sys
import tkinter as tk
import time

TAG_LENGTH = 7
city_names = {} # key = city name, value = tag
coordinates = {} # key = tag, value = (lat, long)
graph = {} # key = tag, value = set of tuples (neighbor, distance)
routes = {} # key = (smaller tag, larger tag), value = line created by canvas
HEIGHT = 800
WIDTH = 1200
lat_max = 0.0
lat_min = 1000.0
long_max = -1000.0
long_min = 0.0

start = time.perf_counter()

# initializing city_names
with open("rrNodeCity.txt") as f:
    for line in [line.strip() for line in f]:
        tag = line[0:7]
        city = line[7:].strip()
        city_names[city] = tag

# initializing coordinates and graph
with open("rrNodes.txt") as f:
    for line in [line.strip() for line in f]:
        arr = line.split()
        tag = arr[0]
        lat = float(arr[1])
        lon = float(arr[2])
        lat_max = max(lat_max, lat)
        lat_min = min(lat_max, lat)
        long_max = max(long_max, lon)
        long_min = min(long_min, lon)
        coordinates[tag] = (lat, lon)
        graph[tag] = set()

# initializing graph continued
with open("rrEdges.txt") as f:
    for line in [line.strip() for line in f]:
        arr = line.split()
        tag0 = arr[0]
        tag1 = arr[1]
        distance = calcd(coordinates[tag0], coordinates[tag1])
        graph[tag0].add((tag1, distance))
        graph[tag1].add((tag0, distance))

end = time.perf_counter()
print("Time to create data structures: %s" % (end - start))

def dij(start, end, r, c): # start and end are ids
    count = 0
    closed = set()
    fringe = []
    # store in form (distance, (path))
    heappush(fringe, (0.0, (start, ))) 
    while len(fringe) != 0:
        state = heappop(fringe)
        if state[1][0] == end:
            for i in range(0, len(state[1]) - 1):
                c.itemconfig(routes[(min(state[1][i], state[1][i + 1]), max(state[1][i], state[1][i + 1]))], fill = "green", width = "3")
            r.update()
            return state[1] # returns the distance
        if state[1][0] not in closed:
            closed.add(state[1][0])
            for neighbor, distance in graph[state[1][0]]:
                if neighbor not in closed:
                    c.itemconfig(routes[(min(state[1][0], neighbor), max(state[1][0], neighbor))], fill = "red") # changes color of one line to red
                    if count % 2000 == 0:
                        r.update()
                    count += 1
                    tup = (
                        state[0] + distance,
                        (neighbor, ) + state[1]
                    )
                    heappush(fringe, tup)
    return None

def a_star(start, end, r, c): # start and end are ids
    count = 0
    closed = set()
    fringe = []
    # store in form (heuristic, distance, (path))
    heappush(fringe, (calcd(coordinates[start], coordinates[end]), 0.0, (start, ))) 
    while len(fringe) != 0:
        state = heappop(fringe)
        if state[2][0] == end:
            for i in range(0, len(state[2]) - 1):
                c.itemconfig(routes[(min(state[2][i], state[2][i + 1]), max(state[2][i], state[2][i + 1]))], fill = "green", width = "3")
            r.update()
            return state[2] # returns the distance
        if state[2][0] not in closed:
            closed.add(state[2][0])
            for neighbor, distance in graph[state[2][0]]:
                if neighbor not in closed:
                    c.itemconfig(routes[(min(state[2][0], neighbor), max(state[2][0], neighbor))], fill="blue") # changes color of one line to blue
                    if count % 2000 == 0:
                        r.update()
                    count += 1
                    tup = (
                        state[1] + distance + calcd(coordinates[neighbor], coordinates[end]),
                        state[1] + distance,
                        (neighbor, ) + state[2]
                    )
                    heappush(fringe, tup)
    return None

def convert(coordinates):
    y, x = coordinates # (lat, long)
    x_new = WIDTH / (long_max - long_min) * (x - long_min)
    y_new = HEIGHT - HEIGHT / (lat_max - lat_min) * (y - lat_min)
    return (x_new, y_new)

def create_routes(c):
    for city, neighbors in graph.items():
        for neighbor, distance in neighbors:
            if city < neighbor:
                line = c.create_line([convert(coordinates[city]), convert(coordinates[neighbor])], tag = "train_route")
                routes[(city, neighbor)] = line

# def create_grid(c):
# 	# create all horizontal lines
# 	for i in range(0, WIDTH, 8):
# 		for j in range(0, HEIGHT, 8):
# 			line = c.create_line([(i, j), (i+8, j)], tag='grid_line')
# 			lines.append(line)


# 	# Creates all vertical lines
# 	for i in range(0, WIDTH, 8):
# 		for j in range(0, HEIGHT, 8):
# 			line = c.create_line([(j, i), (j, i+8)], tag='grid_line')
# 			lines.append(line)

# def make_red(r, c): # makes all the lines red
# 	for line in lines:
# 		c.itemconfig(line, fill="red") # changes color of one line to red
# 		r.update() # update frame
# 		# time.sleep(0.1)


root = tk.Tk() # creates the frame

def on_closing():
    root.destroy()
    root2 = tk.Tk() # creates the frame

    canvas = tk.Canvas(root2, height=HEIGHT * 4 / 3, width=WIDTH, bg='white') # creates a canvas widget, which can be used for drawing lines and shapes
    create_routes(canvas)
    canvas.pack(expand = True) # packing widgets places them on the board

    start = time.perf_counter()
    distance1 = a_star(city_names[city1], city_names[city2], root2, canvas)
    end = time.perf_counter()
    
    print("%s to %s with A*: %s seconds." % (city1, city2, (end - start)))

root.protocol("WM_DELETE_WINDOW", on_closing)

canvas = tk.Canvas(root, height=HEIGHT * 4 / 3, width=WIDTH, bg='white') # creates a canvas widget, which can be used for drawing lines and shapes
create_routes(canvas)
canvas.pack(expand = True) # packing widgets places them on the board

city1 = sys.argv[1]
city2 = sys.argv[2]

start1 = time.perf_counter()
distance1 = dij(city_names[city1], city_names[city2], root, canvas)
end1 = time.perf_counter()

# start2 = time.perf_counter()
# distance2 = a_star(city_names[city1], city_names[city2])
# end2 = time.perf_counter()

print("%s to %s with Dijkstra: %s seconds." % (city1, city2, (end1 - start1)))

root.mainloop()
