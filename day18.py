from functools import reduce
import numpy as np
import portion as P

def getOffset(line):
    match line:
        case ('R', count, color):
            return np.array((int(0), int(count)))
        case ('L', count, color):
            return np.array((0, -int(count)))
        case ('U', count, color):
            return np.array((-int(count), 0))
        case ('D', count, color):
            return np.array((int(count), 0))

def getOffset2(line):
    count = int(line[2][2:7], 16)
    match line[2][7]:
        case '0':
            return np.array((int(0), int(count)))
        case '1':
            return np.array((int(count), 0))
        case '2':
            return np.array((0, -int(count)))
        case '3':
            return np.array((-int(count), 0))
        
def rowSpan(seg):
    x0 = seg[0][0]
    x1 = seg[1][0]
    return (min(x0, x1), max(x0, x1))

def contains(span, x):
    return x >= span[0] and x <= span[1]

def direction(seg):
    x0 = seg[0][0]
    x1 = seg[1][0]
    if x0 == x1:
        return 0
    elif x0 < x1:
        return 1
    else:
        return -1
    
def dirChanges(segs):
    last = 0
    count = 0
    locations = []
    started = False
    for seg in segs:
        dire = direction(seg)
        if dire != last:
            count += 1
            locations.append(seg[0][1])
            started = not started
        elif dire == last and dire != 0 and not started:
            locations[-1] = seg[0][1]
        last = dire
    return locations

def union(regions1, regions2):
    p = P.empty()
    for a,b in regions1:
        p = p | P.closed(a,b)
    for a,b in regions2:
        p = p | P.closed(a,b)
    ret = []
    for r in p:
        ret.append((r.lower, r.upper))
    return ret

def countRowPixels(segs, i):
    rowsegs = list(filter(lambda x: direction(x) != 0 and contains(rowSpan(x), i), segs))
    rowlines = [(min(x[0][1], x[1][1]), max(x[0][1], x[1][1])) for x in filter(lambda x: direction(x) == 0 and x[0][0] == i, segs)]
    rowsegs.sort(key=lambda x: x[0][1])
    regs = dirChanges(rowsegs)
    regs = list((a,b) for a,b in zip(regs[::2],regs[1::2]))
    regs = union(regs, rowlines)
    internal = list(b-a+1 for a,b in regs)
    filled = sum(internal)
    return filled
    
def countPixels(segs, bounds):
    total = 0
    criticalRows = list(set(vvert for seg in segs for vert in seg for vvert in [vert[0], vert[0]+1, vert[0]-1] if vvert >= 0))
    criticalRows.sort()
    pixcounts = {}
    for row, nextr in zip(criticalRows, criticalRows[1:]):
        total += (nextr-row)*countRowPixels(segs, row)
    return total
    
def getSegmentsAndBounds(data, part2=False):
    cur = np.array((0, 0))
    pairs = []
    minBounds = np.array((0, 0))
    bounds = np.array((0, 0))
    for line in data:
        ofst = getOffset(line) if not part2 else getOffset2(line)
        next = cur+ofst
        pairs.append((cur, next))
        cur = next
        bounds = np.maximum(bounds, cur)
        minBounds = np.minimum(minBounds, cur)
    bounds += np.array((1,1))
    bounds -= minBounds
    for idx, pair in enumerate(pairs):
        pairs[idx] = (pair[0]-minBounds, pair[1]-minBounds)
    return (pairs, bounds)

with open("input18") as f:
    data = [line[:-1].split(' ') for line in f.readlines()]
    
    pairs, bounds = getSegmentsAndBounds(data, False)
    painted = countPixels(pairs, bounds)
    
    print("part1", painted)
    
    pairs, bounds = getSegmentsAndBounds(data, True)
    painted = countPixels(pairs, bounds)
    
    print("part2", painted)
