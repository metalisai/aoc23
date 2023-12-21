import math
import numpy as np

offsets = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def safeSample(gmap, pos):
    loc = repeat(gmap, pos)
    return gmap[loc[0]][loc[1]]

def repeat(gmap, pos):
    return (pos[0]%len(gmap), pos[1]%len(gmap[0]))

def printMap(mmap):
    print("\n".join([" ".join([str(num).zfill(1) for num in line]) for line in mmap]))
    
def printOpen(mmap, oset):
    em = [[c for c in line] for line in mmap]
    rcount = 0
    for val in oset:
        if val[0] >= 0 and val[0] < len(mmap) and val[1] >= 0 and val[1] < len(mmap[0]):
            em[val[0]][val[1]] = "x"
            rcount += 1
    #for line in em:
        #print("".join(line))
    #print("REACHED", rcount)
    return rcount
    
def copyMap(mmap):
    return [[num for num in line] for line in mmap]

def emptyMap(mmap):
    return [[0 for num in line] for line in mmap]

def traverse(gmap, countmap, steps, start):
    prevCountMap = copyMap(countmap)
    curCountMap = copyMap(countmap)
    curCountMap[start[0][0]][start[0][1]] = 1
    
    openSet = set(start)
    for xx in range(steps):
        targetMap = emptyMap(countmap)
        
        nextS = set([])
        for v in openSet:
            for o in offsets:
                nextP = (o[0]+v[0], o[1]+v[1])
                s = safeSample(gmap, nextP)
                if s == "#":
                    continue
                nextS.add(nextP)
        openSet = nextS
        
    rcount = printOpen(gmap, openSet)
    return len(openSet), rcount

def findStart(gmap):
    for row, line in enumerate(gmap):
        for col, c in enumerate(line):
            if c == "S":
                return (row, col)
            
with open("input21") as f:
    lines = [[c for c in line] for line in f.read().splitlines()]
    start = findStart(lines)
    countmap = [[0 for c in line] for line in lines]
    countmap[start[0]][start[1]] = 1
    part1, _ = traverse(lines, countmap, 64, [findStart(lines)])
    print("part1", part1)
    
    _, reachableInCell = traverse(lines, countmap, 131, [findStart(lines)])
    bestAttempt = (((26501365*2+1)/131)**2 * 0.5) * reachableInCell
    print("I RESIGN", bestAttempt)
    
    if True:
        xs = np.array(range(101, 300, 50))
        A = np.vstack([xs**2, xs, (xs-1)**2, (xs-1), np.ones_like(xs)]).T
        ys = np.array([traverse(lines, countmap, x, [findStart(lines)])[0] for x in xs])
        b = ys.reshape(-1, 1)
        cfs = np.linalg.lstsq(A, b, rcond=None)[0].flatten()
        fun = lambda x: cfs[0]*x*x + cfs[1]*x + cfs[2]*(x-1)*(x-1) + cfs[3]*(x-1) + cfs[4]
        print("part2?", fun(26501365))
        # this doesn't fit either (^.^)>-|o  |  <-door
