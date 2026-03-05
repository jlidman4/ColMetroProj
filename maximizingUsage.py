#List of parameters in this class and their meanings:
#piDX = Total population coverage accumulated so far
#piCX = The total construction cost accumulated so far
#piHX = Number of stations currently on the path
#betaX = The node where path currently ends
#xiX = Preceding node on the path


import math

completedList = []
activeList = []

class LsubX:
    def __init__(self, piDX, piCX, piHX, betaX, xiX):
        self.piDX = piDX 
        self.piCX = piCX 
        self.piHX = piHX
        self.betaX = betaX
        self.xiX = xiX
    
    def compare(self, path):
        same = False
        samePop = (self.piDX == path.piDX)
        sameCost = (self.piCX == path.piCX)
        sameStationNumber = (self.piHX == path.piHX)
        sameEndStation = (self.betaX == path.betaX)
        sameStartStation = (self.xiX == path.xiX)
        if(samePop and sameCost and sameStationNumber and sameEndStation and sameStartStation):
            same = True
        return same
        

def isDominated(LsubX1, LsubX2):
    dominated = False
    stations = (LsubX2.piHX <= LsubX1.piHX)
    popCoverage = (LsubX2.piDX >= LsubX1.piDX)
    constCost = (LsubX2.piCX <= LsubX1.piCX)
    strictlyBetter = (LsubX2.piHX < LsubX1.piHX) or (LsubX2.piDX > LsubX1.piDX) or (LsubX2.piCX < LsubX1.piCX)
    if(stations and popCoverage and constCost and strictlyBetter):
        dominated = True
    return dominated

def checkHopCount(path, maxStations):
    check = True
    if(path.piHX >= maxStations):
        check = False
    return check

def square(num1):
    return num1*num1

def calculateDistance(pointOne, pointTwo):
    return math.sqrt(square(pointTwo.x-pointOne.x) + square(pointTwo.y - pointOne.y))

def validityCheck(xiX, node, D):
    valid = False
    if(calculateDistance(xiX, node) >= D):
        valid = True
    return valid

def createNewPath(oldPath, partialPath):
    newPopulation = partialPath.piDX + oldPath.piDX
    newCost = partialPath.piCX + oldPath.piCX
    newAmountStations = oldPath.piHX + 1
    toReturn = LsubX(newPopulation, newCost, newAmountStations, partialPath.betaX, oldPath.betaX)
    return toReturn

def isComparable(pathOne, pathTwo):
    comparable = False
    if(pathOne.betaX == pathTwo.betaX):
        comparable = True
    return comparable

def pruning(actList, pathCompare):
    removeList = []
    toAdd = True
    for i in range(0,(len(actList))):
        path = actList[i]
        if((not pathCompare.compare(path))):
            if isComparable(pathCompare, path):
                if(isDominated(pathCompare, path)):
                    toAdd = False
    if(toAdd):
        for i in range(0,(len(actList))):
            p = actList[i]
            if((not pathCompare.compare(p)) and isComparable(pathCompare, p)):
                if(isDominated(p,pathCompare)):
                    removeList.append(p)
        actList.append(pathCompare)
        for remPath in removeList:
            actList.remove(remPath)            
#network_graph is map of all possible stations, populations (d) and construction costs between
#them(c)
#start_station is the node where the dummy station is created
#final_station is the destination node, trigger that moves path from the active list
#to the completed list
#max_stations is the constraint W, used to check if path grown too long
#min_distance is D
def find_optimal_metro_lines(network_graph, start_station, final_station, max_stations, min_distance):
    newPath = LsubX(0,0,1,start_station, start_station)
    activeList.append(newPath)
    while(len(activeList)!=0):
        currPath = activeList.pop(0)
        if(currPath.betaX == final_station):
            completedList.append(currPath)
            continue
        if(checkHopCount(currPath, max_stations)):
            stationList = network_graph[currPath.betaX]
            for station in stationList:
                if((not (station == currPath.xiX)) and validityCheck(currPath.xiX, station, min_distance)):
                    nouveauPath = createNewPath(currPath, station)
                    pruning(activeList, nouveauPath)
        


         
