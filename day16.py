import itertools
import numpy as np
import sys;sys.setrecursionlimit(15000)

dirs = [(0,1),(0,-1),(1,0),(-1,0)]
dirIdx = {(0,1):0, (0,-1):1, (1,0):2, (-1,0):3}

def reflect1(direction):
    return np.array((-direction[1], -direction[0]))

def reflect2(direction):
    return np.array((direction[1], direction[0]))

def traverse(data, beamcount, coord, bdir):
    if coord[0] < 0 or coord[1] < 0 or coord[0] >= len(data) or coord[1] >= len(data[0]):
        return
    if beamcount[coord[0]][coord[1]][dirIdx[tuple(bdir)]] > 0:
        return
    beamcount[coord[0]][coord[1]][dirIdx[tuple(bdir)]] = 1
    
    def traverseTo(data, beamcount, offset):
        traverse(data, beamcount, coord+offset, offset)
    
    match data[coord[0]][coord[1]]:
        case ".":
            traverse(data, beamcount, coord+bdir, bdir)
        case "|":
            if bdir[0] == 0:
                traverseTo(data, beamcount, ( 1, 0))
                traverseTo(data, beamcount, (-1, 0))
            else:
                traverse(data, beamcount, coord+bdir, bdir)
        case "-":
            if bdir[1] == 0:
                traverseTo(data, beamcount, ( 0,  1))
                traverseTo(data, beamcount, ( 0, -1))
            else:
                traverse(data, beamcount, coord+bdir, bdir)
        case "/":
            traverseTo(data, beamcount, reflect1(bdir))
        case "\\":
            traverseTo(data, beamcount, reflect2(bdir))

with open("input16") as f:
    data = [[c for c in line if c != '\n'] for line in f.readlines()]
    beamcountF = lambda: [[[0]*4 for c in line] for line in data]
    beamcount = beamcountF()
    traverse(data, beamcount, np.array((0, 0)), np.array((0, 1)))
    
    energized = sum(any(c) for line in beamcount for c in line)
    print("part1:", energized)
    
    scores = []
    
    down = (((0, i), (1, 0)) for i in range(len(data[0])))
    up = (((len(data)-1, i), (-1, 0)) for i in range(len(data[0])))
    right = (((i, 0), (0, 1)) for i in range(len(data[0])))
    left = (((i, len(data[0])-1), (0, -1)) for i in range(len(data[0])))
    
    for start, direction in itertools.chain(down, up, right, left):
        beamcount = beamcountF()
        traverse(data, beamcount, np.array(start), direction)
        energized = sum(any(c) for line in beamcount for c in line)
        scores.append(energized)
    print("part2:", max(scores))
