from collections import deque
from heapq import heappush, heappop, heapify
from distanceDemo import calcd
import sys
import time

TAG_LENGTH = 7
city_names = {} # key = city name, value = tag
coordinates = {} # key = tag, value = (lat, long)
graph = {} # key = tag, value = set of tuples (neighbor, distance)

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

def dij(start, end): # start and end are ids
    closed = set()
    fringe = []
    # store in form (distance, node)
    heappush(fringe, (0.0, start)) 
    while len(fringe) != 0:
        state = heappop(fringe)
        if state[1] == end:
            return state[0] # returns the distance
        if state[1] not in closed:
            closed.add(state[1])
            for neighbor, distance in graph[state[1]]:
                if neighbor not in closed:
                    tup = (
                        state[0] + distance,
                        neighbor
                    )
                    heappush(fringe, tup)
    return None

def a_star(start, end): # start and end are ids
    closed = set()
    fringe = []
    # store in form (heuristic, distance, node)
    heappush(fringe, (calcd(coordinates[start], coordinates[end]), 0.0, start)) 
    while len(fringe) != 0:
        state = heappop(fringe)
        if state[2] == end:
            return state[1] # returns the distance
        if state[2] not in closed:
            closed.add(state[2])
            for neighbor, distance in graph[state[2]]:
                if neighbor not in closed:
                    tup = (
                        state[1] + distance + calcd(coordinates[neighbor], coordinates[end]),
                        state[1] + distance,
                        neighbor
                    )
                    heappush(fringe, tup)
    return None

city1 = sys.argv[1]
city2 = sys.argv[2]

start1 = time.perf_counter()
distance1 = dij(city_names[city1], city_names[city2])
end1 = time.perf_counter()

start2 = time.perf_counter()
distance2 = a_star(city_names[city1], city_names[city2])
end2 = time.perf_counter()

print("%s to %s with Dijkstra: %s in %s seconds." % (city1, city2, distance1, (end1 - start1)))
print("%s to %s with A*: %s in %s seconds." % (city1, city2, distance2, (end2 - start2)))