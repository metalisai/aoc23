import numpy as np

class Grid:
    skyline=0
    placedBlocks={}
    def __init__(self, hSize, vSize):
        self.grid=np.array([[[0]*hSize for y in range(hSize)] for x in range(vSize)])
    def placeBlock(self, xRange, yRange, zRange, bid):
        supports = self.getSupports(xRange, yRange, zRange[0])
        self.grid[zRange[0]:zRange[1], xRange[0]:xRange[1], yRange[0]:yRange[1]] = bid
        self.placedBlocks[bid] = (xRange, yRange, zRange, supports, bid)
    def printGrid(self):
        print("grid", self.grid)
    def getSkyline(self, xRange, yRange, maxZ):
        ret = 0
        xySlice = self.grid[0:maxZ ,xRange[0]:xRange[1], yRange[0]:yRange[1]]
        nonZero = np.nonzero(xySlice)[0]
        if len(nonZero) != 0:
            ret = np.max(nonZero)+1
        if ret > maxZ:
            raise(Exception("too high"))
        return ret
    def getSupports(self, xRange, yRange, z):
        z = max(z-1, 0)
        ret = np.unique(self.grid[z:z+1, xRange[0]:xRange[1], yRange[0]:yRange[1]])
        if ret[0] == 0:
            ret = ret[1:]
        return ret
    def getBlock(self, bid):
        return self.placedBlocks[bid]
    def getAllBlocks(self):
        return self.placedBlocks.values()

def placeBrick(gridO, brick, bid):
    size = brick[1]-brick[0]+1
    minC = brick[0][0:2]
    maxC = minC + size[0:2]
    if size[0] <= 0 or size[1] <= 0 or size[2] <= 0:
        raise("invalid size")
    grid=gridO.grid
    xRange = (minC[0], maxC[0])
    yRange = (minC[1], maxC[1])
    zRange = (brick[0][2], brick[0][2] + size[2])
    location = gridO.getSkyline(xRange, yRange, zRange[1])
    gridO.placeBlock((minC[0], maxC[0]), (minC[1],maxC[1]), (location, location+size[2]), bid)

def safeToRemove(grid, bid):
    allBlocks = grid.getAllBlocks()
    for block in allBlocks:
        if bid in block[3] and len(block[3]) == 1:
            return False
    return True

def getExclusiveDependencies(grid, bid, dependencies):
    allBlocks = grid.getAllBlocks()
    for block in allBlocks:
        if block[4] not in dependencies and bid in block[3] and not any(b not in dependencies for b in block[3]):
            dependencies.add(block[4])
            getExclusiveDependencies(grid, block[4], dependencies)
    return dependencies

with open("input22") as f:
    grid = Grid(10, 512)
    
    data = [line.split('~') for line in f.read().splitlines()]
    data = [[np.array([int(nr) for nr in end.split(',')]) for end in line] for line in data]
    
    data = sorted(data, key=lambda x: x[1][2])
    
    for idx, brick in enumerate(data):
        placeBrick(grid, brick, idx+1)
    safes = [safeToRemove(grid, idx+1) for idx in range((len(data)))]
    print("part1", sum(safes))
    # slow but I really can't anymore, could've made a graph or something
    dependencies = [len(getExclusiveDependencies(grid, idx+1, set([idx+1])))-1 for idx in range((len(data)))]
    print("part2", sum(dependencies))
