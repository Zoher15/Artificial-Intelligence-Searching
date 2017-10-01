#!/usr/bin/env python3

# put your routing program here!

# Last Update : September 23, 2017
# Author : Dhaval R Niphade
# Course : CSCI B551 Elements of Artificial Intelligence
# Assignment 1 - Question 1

'''
1. A* & BFS work the best among the choice of algorithms. A*'s performance can be improved even further by assigning weights to the individual
    scenarios where we compute the heuristic values. It yields an answer in the fastest time for routes that are deeper within the graph.
    BFS outperforms A* and DFS when the route is shorter since it explores each adjacent city level by level.

2. A comparison between the algorithms can be drawn in the following fashion:
    For short routes
        A* = 0.002s
        Uniform = 0.0009s
        BFS = 0.0s
        DFS = 0.0s

    For long routes
        A* = 0.29s
        Uniform = 0.38s
        BFS = 0.34s
        DFS = 0.73s

    As observed A* performs better when the cities are further apart.

3.  DFS runs out of memory when it embarks upon a path that is much longer than the one from its next child within the fringe.
    BFS, Uniform and A* require the least amount of memory for short routes. As the route span longer BFS and Uniform grow equally
    as bad as DFS.

4. The heuristic used was the Great Circle Distance. The performance can be improved by assigning weights to the heuristic values
    that we compute.
    For specific cost functions we can modidfy the percentage that we optimize the heuristic based on how many turns we have already taken.
'''

#IMPORT Items

import math,sys,time
from collections import defaultdict

#Global variables
highwayHash = defaultdict(set)  #Hash map for cities and their corresponding highways
cityHash = {}     #Hash map for cities and their corresponding objects
source, dest, routeAlgo, costFunc = str,str,str,str   #User input from command line
averageSpeed = 0


#SECTION 1 - BUILD LIST OF TUPLES

def buildTuple(line,mode):
    if(str(mode)=='city'):
        city_name,lat,long = line.split()
        return(str(city_name),float(lat),float(long))
    if(str(mode)=='road'):
        temp = line.split()
        if(len(temp)==5):
            startCity,endCity,dist,speedLimit,highway = temp[0],temp[1],temp[2],temp[3],temp[4]
        else:
            startCity, endCity, dist, speedLimit, highway = temp[0], temp[1], temp[2], float(45) , temp[3]
        return (str(startCity),str(endCity),float(dist),float(speedLimit),str(highway))


#SECTION 2 - DEFINE CLASSES AND MEMBER FUNCTIONS

class City(object):

    def __init__(self,name,latitude,longitude):
        self.name,self.latitude,self.longitude = name,latitude,longitude

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

class Highway(object):

    def __init__(self,start,end,dist,speedLimit,name):
        self.name = name
        self.start = start
        self.end = end
        self.dist = float(dist)
        self.speedLimit = float(speedLimit)

#SECTION 3 - BUILD THE GRAPH
# Build the graph

def buildGraph(cityInfo,roadSegs):

    allCities,allRoads = set(),set()    #Make sets of both
    global highwayHash, cityHash, allPaths  #Access global values

    tempSpeed,count = 0,0

    for highways in roadSegs:
        if(len(highways)==5) and float(highways[3]):
            allRoads.add(Highway(highways[0],highways[1],highways[2],highways[3],highways[4]))
            tempSpeed+=float(highways[3])   #Sum up all the speeds
            allCities.add(highways[0])  #Get unique cities as well - start
            allCities.add(highways[1])  #Get unique cities as well - end

    global averageSpeed
    averageSpeed = tempSpeed / len(allRoads)

    for cities in allCities:    #For all unique cities find if one is missing from the txt file
        if cities not in (city[0] for city in cityInfo):
            cityInfo.append([cities,None,None])   #Some city is connected by a highway but its latitude and longitude are unknown

    #Build city map
    for row in cityInfo:
        lat = float(row[1]) if row[1]  else 0.0 # 'Get values or default to 0'  #Unnecessary
        long =float(row[2]) if row[2]  else 0.0 # 'Get values or default to 0'  #Unnecessary
        city_obj = City(row[0], float(row[1]) if row[1] else 0.0,float(row[2]) if row[2] else 0.0)
        cityHash[row[0]]=city_obj   # 'Feed Hash table with city name as key and city object as value'

    for keys in cityHash:
        highwayHash[keys] = filter(None,{high_obj if high_obj.start == keys or high_obj.end==keys else None for high_obj in allRoads})  #'For each city as key create a correspondin list of highways it has from the given list of highways

    print("\nGraph Building complete")

    return

#SECTION 4 - Helper functions
def getGCD(source, destination):
    latSource,longSource ,latDest, longDest = map(math.radians,[cityHash[source].latitude, cityHash[source].longitude, cityHash[dest].longitude, cityHash[dest].longitude])

    latDiff = latSource - latDest
    longDiff = longSource - longDest

    hsine = math.sin(latDiff / 2) ** 2 + math.cos(latSource) * math.cos(latDest) * math.sin(longDiff / 2) ** 2

    return 6371 * 2 * math.asin(math.sqrt(hsine))
    # Formula obtained from Wikipedia for Great Circle Distance - Original source Admirality Manual of Navigation, Volume 1


#SECTION 5 - Implement Routing Algorithms
def findBFS(source,destination,costFunc):
    print("Running BFS....")
    fringe = [(0, 0, [source])]
    visited = []

    while(fringe):
        successor = fringe.pop(0)
        path = successor[2]
        currentCity = path[-1]
        if(currentCity not in visited):
            if(currentCity == destination):
                # print(path)
                return successor

            for edges in highwayHash[currentCity]:
                nextCity = edges.start if edges.end == currentCity else edges.end if edges.start == currentCity  else None
                newPath = list(path)
                newPath.append(nextCity)
                if(nextCity not in x[0] for x in fringe):
                    fringe.append((successor[0] + edges.dist, successor[1] + edges.speedLimit,newPath))
            visited.append(currentCity)
    print("Path not found! Please try again")
    return None

def findDFS(source,destination,costFunc):
    print("Running DFS...")
    # fringe = [(0,0,[source])]
    fringe = [(0, 0, [source], getGCD(source, destination), 0, 0)]  # Tuple of Distance, SpeedLimit, Haversine, Turns, Time
    visited = []

    while (fringe):
        successor = fringe.pop()
        path = successor[2]  # Get current city from object that we just popped
        currentCity = path[-1]
        if (currentCity not in visited):
            if (currentCity == destination):  # Found the destination - proceed to calculations
                # print(path)
                return successor

            for edges in highwayHash[currentCity]:
                nextCity = edges.start if edges.end == currentCity else edges.end if edges.start == currentCity  else None
                newPath = list(path)
                newPath.append(nextCity)
                if (nextCity not in x[0] for x in fringe):
                    fringe.append((successor[0]+edges.dist, successor[1]+edges.speedLimit, newPath))
            visited.append(currentCity)
    print("Path not found! Please try again")
    return None


def findUniform(source,destination,costFunc):
    print("Running Uniform....")
    # fringe = [(getGCD(source,destination),[source],0,0)]
    fringe = [(0,0,[source],getGCD(source,destination),0,0)]    # Tuple of Distance, SpeedLimit, Path, Haversine, Turns, Time
    visited = []

    while(fringe):

        if(str(costFunc)=="segment"):
            fringe.sort(key=lambda tup: tup[4])
        elif(str(costFunc)=="distance"):
            fringe.sort(key=lambda tup: tup[0])
        elif (str(costFunc) == "time"):
            fringe.sort(key=lambda tup: tup[5])

        successor = fringe.pop(0)
        path = successor[2]
        currentCity = path[-1]
        if(currentCity not in visited):
            if(currentCity == destination):
                # print(path)
                return successor
            for edges in highwayHash[currentCity]:
                nextCity = edges.start if edges.end == currentCity else edges.end if edges.start == currentCity  else None
                newPath = list(path)
                newPath.append(nextCity)
                if(nextCity not in x[0] for x in fringe):
                    # fringe.append((successor[0] + getGCD(nextCity, destination), newPath, successor[2] + 1,successor[3] + edges.dist / edges.speedLimit))
                    fringe.append((successor[0] + edges.dist, successor[1]+edges.speedLimit, newPath,successor[3] + getGCD(nextCity, destination),successor[4] + 1,successor[5] + edges.dist / edges.speedLimit))
            visited.append(currentCity)
    print("Path not found! Please try again")
    return None

def findAstar(source,destination,costFunc):
    print("Running AStar....")
    gcd = getGCD(source, destination)
    # fringe = [(gcd, [source], 0, 0)]
    fringe = [(0, 0, [source], getGCD(source, destination), 0, 0)]  # Tuple of Distance, SpeedLimit, Path, Haversine, Turns, Time
    visited = set()

    while (fringe):

        if (str(costFunc) == "segment"):
            fringe.sort(key=lambda tup: tup[4])
        elif (str(costFunc) == "distance"):
            fringe.sort(key=lambda tup: tup[3])
        elif (str(costFunc) == "time"):
            fringe.sort(key=lambda tup: tup[5])
        successor = fringe.pop(0)
        path = successor[2]
        currentCity = path[-1]
        if (currentCity not in visited):
            if (currentCity == destination):
                # print(path)
                return successor
            for edges in highwayHash[currentCity]:
                nextCity = edges.start if edges.end == currentCity else edges.end if edges.start == currentCity  else None
                newPath = list(path)
                newPath.append(nextCity)

                # Calculate heuristic
                hs = getGCD(nextCity,destination)

                # Check cost function and update costs/priorities
                # Add weights to the priorities incase we need to optimize towards a specific goal

                if (str(costFunc) == "segment"):    #Fewest Turns
                    if (nextCity not in x[0] for x in fringe):
                        # fringe.append((successor[0] + getGCD(nextCity, destination), newPath, successor[2] + hs, successor[3] + edges.dist / edges.speedLimit))
                        fringe.append((successor[0] + edges.dist, successor[1] + edges.speedLimit, newPath,successor[3] + getGCD(nextCity, destination), successor[4] + 1 + hs,successor[5] + edges.dist / edges.speedLimit))
                if (str(costFunc) == "distance"):  # Fewest Least Distance travelled
                    if (nextCity not in x[0] for x in fringe):
                        # fringe.append((successor[0] + getGCD(nextCity, destination) + hs, newPath, successor[2] + 1, successor[3] + edges.dist / edges.speedLimit))
                        fringe.append((successor[0] + edges.dist, successor[1] + edges.speedLimit, newPath,successor[3] + getGCD(nextCity, destination) + hs, successor[4] + 1,successor[5] + edges.dist / edges.speedLimit))
                if (str(costFunc) == "time"):  # Least time required
                    if (nextCity not in x[0] for x in fringe):
                        # fringe.append((successor[0] + getGCD(nextCity, destination), newPath, successor[2] + 1, successor[3] + edges.dist / edges.speedLimit + hs))
                        fringe.append((successor[0] + edges.dist, successor[1] + edges.speedLimit, newPath,successor[3] + getGCD(nextCity, destination), successor[4] + 1,successor[5] + edges.dist / edges.speedLimit + hs))
                visited.add(currentCity)

    print("Path not found! Please try again")
    return None

def PrintResult(source,dest,costFunc, route):
    # print(route)
    return

#SECTION 0 - DRIVER Functions
def main():
    print("Reading files")
    cityInfo = [buildTuple(line, 'city') for line in open('city-gps.txt', 'r')]
    roadSegs = [buildTuple(line, 'road') for line in open('road-segments.txt', 'r')]
    print("Files read.....Advancing to graph generation")
    global source, dest, routeAlgo, costFunc
    source,dest,routeAlgo,costFunc = sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4]
    buildGraph(cityInfo,roadSegs)

    # route = findDFS(source, dest, costFunc)
    # route = findBFS(source,dest,costFunc)
    # route = findUniform(source,dest,"time")
    # route = findAstar(source, dest, "segment")

    startTime = time.time()

    #Call appropriate function
    if(str(routeAlgo) == "bfs"):
        route = findBFS(source,dest,costFunc)
        distance, totalTime = route[0], route[0]/averageSpeed
        print(distance," ",totalTime," "," ".join(route[2]))
    elif(str(routeAlgo) == "dfs"):
        route = findDFS(source, dest, costFunc)
        distance, totalTime = route[0], route[0] / averageSpeed
        print(distance, " ", totalTime, " ", " ".join(route[2]))
    elif(str(routeAlgo) == "uniform"):  # Tuple of Distance, SpeedLimit, Path, Haversine, Turns, Time
        route = findUniform(source,dest,costFunc)
        distance, totalTime = route[0], route[0] / averageSpeed
        print(distance, " ", totalTime, " ", " ".join(route[2]))
    else:
        route = findAstar(source,dest,costFunc)     # Tuple of Distance, SpeedLimit, Path, Haversine, Turns, Time
        distance, totalTime = route[0], route[0] / averageSpeed
        print(distance, " ", totalTime, " ", " ".join(route[2]))

    # print("Total time required for the algorithm : ", time.time() - startTime)

    #Pretty print everything
    return 0

if __name__ == '__main__':
    print("Commencing program.....")
    main()


