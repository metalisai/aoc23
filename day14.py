import math
from collections import deque
import random

def sample(data, coord):
    if coord[0] < 0 or coord[0] >= len(data) or coord[1] < 0 or coord[1] >= len(data[0]):
        return '#'
    return data[coord[0]][coord[1]]

def iterator(data):
    return ((row, col) for row in range(len(data)) for col in range(len(data[0])))

def rollRocks(data, dir):
    indices = iterator(data)
    for row, col in indices:
        dirIdx = (row+dir[0], col+dir[1])
        if sample(data, (row, col)) == 'O' and sample(data, dirIdx) == '.':
            data[row][col] = '.'
            data[dirIdx[0]][dirIdx[1]] = 'O'
            
def rollUntilSettle(data, dir):
    last = None
    current = toString(data)
    while current != last:
        last = current
        rollRocks(data, dir)
        current = toString(data)
    return data
            
def calcLoad(data):
    ret = 0
    for row, col in iterator(data):
        if sample(data, (row, col)) == 'O':
            ret += len(data)-row
    return ret

cache = {}

def cycle_(data, count):
    data = copy(data)
    for i in range(count):
        rollUntilSettle(data,(-1, 0))
        rollUntilSettle(data,(0, -1))
        rollUntilSettle(data,(1, 0))
        rollUntilSettle(data,(0, 1))
    return data

def decompose(n):
    powers = deque()
    for p in range(n.bit_length(), -1, -1):
        power = 1 << p
        if n & power:
            powers.append(power)
    return powers

def cycle(data, count):
    data = copy(data)
    mapStr = toString(data)
    input = mapStr+str(count)
    if input in cache:
        return cache[input]
    elif count == 0:
        return data
    if count == 1:
        if not count == 1:
            raise Exception("wut")
        data = cycle_(data, 1)
    elif not math.log2(count).is_integer():
        decomposed = decompose(count)
        for p2 in decomposed:
            data = cycle(data, p2)
    else:
        data = cycle(data, count//2)
        data = cycle(data, count//2)
    cache[input] = copy(data)
    return data

def toString(data):
    return '\n'.join([''.join(line) for line in data])

def copy(data):
    return [[c for c in data[row]] for row in range(len(data))]
    
with open("input14") as f:
    data = [[c for c in x[:-1]] for x in f.readlines()]
    data2 = copy(data)
    rollUntilSettle(data, (-1, 0))
    print("part1", calcLoad(data))
    data2 = cycle(data2, 1000000000)
    print("part2", calcLoad(data2))
