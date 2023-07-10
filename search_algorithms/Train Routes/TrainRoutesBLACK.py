# Isabella Zhu
# Animation showing Dijkstra, A*, DFS Search Algorithms
# Blue = fringe, Red = visited, Black = unvisited, Green = final path

from collections import deque
from heapq import heappush, heappop, heapify
from distanceDemo import calcd
import sys
import tkinter as tk
from tkinter import *
import time
import os
from functools import partial

TAG_LENGTH = 7
fps = 100
city_names = {} # key = city name, value = tag
coordinates = {} # key = tag, value = (lat, long)
graph = {} # key = tag, value = set of tuples (neighbor, distance)
routes = {} # key = (smaller tag, larger tag), value = line created by canvas
HEIGHT = 450
WIDTH = 900
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
    edges_on_fringe = {} # [node on fringe] = set(neighbors connecting to it)
    # store in form (distance, (path))
    heappush(fringe, (0.0, (start, ))) 
    while len(fringe) != 0:
        state = heappop(fringe)
        if state[1][0] in edges_on_fringe:
            for neighbor in edges_on_fringe[state[1][0]]:
                c.itemconfig(routes[(min(state[1][0], neighbor), max(state[1][0], neighbor))], fill = "red")
        if state[1][0] == end:
            for i in range(0, len(state[1]) - 1):
                c.itemconfig(routes[(min(state[1][i], state[1][i + 1]), max(state[1][i], state[1][i + 1]))], fill = "green", width = "3")
            r.update()
            return state[1] # returns the distance
        if state[1][0] not in closed:
            closed.add(state[1][0])
            for neighbor, distance in graph[state[1][0]]:
                if neighbor not in closed:
                    c.itemconfig(routes[(min(state[1][0], neighbor), max(state[1][0], neighbor))], fill = "blue")
                    if neighbor in edges_on_fringe:
                        edges_on_fringe[neighbor].add(state[1][0])
                    else:
                        edges_on_fringe[neighbor] = {state[1][0]}
                    if count % fps == 0:
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
    edges_on_fringe = {} # [node on fringe] = neighbor connecting to it
    # store in form (heuristic, distance, (path))
    heappush(fringe, (calcd(coordinates[start], coordinates[end]), 0.0, (start, ))) 
    while len(fringe) != 0:
        state = heappop(fringe)
        if state[2][0] in edges_on_fringe:
            for neighbor in edges_on_fringe[state[2][0]]:
                c.itemconfig(routes[(min(state[2][0], neighbor), max(state[2][0], neighbor))], fill = "red")
        if state[2][0] == end:
            for i in range(0, len(state[2]) - 1):
                c.itemconfig(routes[(min(state[2][i], state[2][i + 1]), max(state[2][i], state[2][i + 1]))], fill = "green", width = "3")
            r.update()
            return state[2] # returns the distance
        if state[2][0] not in closed:
            closed.add(state[2][0])
            for neighbor, distance in graph[state[2][0]]:
                if neighbor not in closed:
                    c.itemconfig(routes[(min(state[2][0], neighbor), max(state[2][0], neighbor))], fill="blue") 
                    if neighbor in edges_on_fringe:
                        edges_on_fringe[neighbor].add(state[2][0])
                    else:
                        edges_on_fringe[neighbor] = {state[2][0]}
                    if count % fps == 0:
                        r.update()
                    count += 1
                    tup = (
                        state[1] + distance + calcd(coordinates[neighbor], coordinates[end]),
                        state[1] + distance,
                        (neighbor, ) + state[2]
                    )
                    heappush(fringe, tup)
    return None

def DFS(start, end, r, c): # start and end are ids
    count = 0
    closed = set()
    fringe = deque([(start, )]) 
    while len(fringe) != 0:
        state = fringe.pop()
        if state[0] == end:
            for i in range(0, len(state) - 1):
                c.itemconfig(routes[(min(state[i], state[i + 1]), max(state[i], state[i + 1]))], fill = "green", width = "3")
            r.update()
            return state[0]
        for neighbor, distance in graph[state[0]]:
            if neighbor not in closed:
                closed.add(neighbor)
                c.itemconfig(routes[(min(state[0], neighbor), max(state[0], neighbor))], fill = "red")
                if count % fps == 0:
                    r.update()
                count += 1
                fringe.append((neighbor, ) + state)
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

root = tk.Tk() # creates the frame

img = PhotoImage(file="image.png")   

def onRestart():
    os.execv(sys.executable, ['python'] + sys.argv)

def updateFPS(val):
    global fps
    fps = int(val)

def onSubmit(canvas, start, des, alg):
    canvas.destroy()
    canvas2 = tk.Canvas(root, height=HEIGHT * 4 / 3, width=WIDTH) # creates a canvas widget, which can be used for drawing lines and shapes
    canvas2.create_image(-150, -75, anchor=NW, image=img)
    create_routes(canvas2)
    label = Label(root, text = "Adjust speed here", background = "white").place(x = WIDTH * 0.05, y = HEIGHT * 0.98)
    slider = Scale(
        root,
        from_ = 100,
        to = 2000,
        orient = 'horizontal',
        background = "white",
        variable = fps,
        command = updateFPS,
    ) 
    slider.place(x = WIDTH * 0.05, y = HEIGHT * 1.05)
    restart_button = Button(root, text = "Restart", activebackground = "black", activeforeground = "white", command = onRestart).place(x = WIDTH * 0.05, y = HEIGHT * 1.2)
    canvas2.pack()
    if alg.get() == "D":
        dij(city_names[start.get()], city_names[des.get()], root, canvas2)
    elif alg.get() == "A":
        a_star(city_names[start.get()], city_names[des.get()], root, canvas2)
    elif alg.get() == "DF":
        DFS(city_names[start.get()], city_names[des.get()], root, canvas2)


# GUI elements
canvas = tk.Canvas(root, height=HEIGHT * 4 / 3, width=WIDTH) # creates a canvas widget, which can be used for drawing lines and shapes
start = Label(root, text = "Start").place(x = WIDTH * 0.35, y = HEIGHT * 0.35)
destination = Label(root, text = "Destination").place(x = WIDTH * 1 / 3, y = HEIGHT * 0.5)
algorithm = Label(root, text = "Algorithm: D = Dijkstra, A = A* Star, DF = DFS").place(x = WIDTH * 0.13, y = HEIGHT * 0.65)
start2 = Entry(start)
start2.place(x = WIDTH * 0.43, y = HEIGHT * 0.35)
destination2 = Entry(destination)
destination2.place(x = WIDTH * 0.43, y = HEIGHT * 0.5)
algorithm2 = Entry(algorithm)
algorithm2.place(x = WIDTH * 0.43, y = HEIGHT * 0.65)
onS = partial(onSubmit, canvas, start2, destination2, algorithm2)
submit_button = Button(root, text = "Find Path", activebackground = "black", activeforeground = "white", command = onS).place(x = WIDTH * 0.5, y = HEIGHT * 0.8)
canvas.pack(expand = True) # packing widgets places them on the board
root.mainloop()