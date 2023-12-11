def getColumn(obs, idx):
    ret = []
    for line in obs:
        ret.append(line[idx])
    return ret

def findExpansions(obs):
    ret = [[],[]]
    for li, line in enumerate(obs):
        if (all([x == '.' for x in line])):
            ret[0].append(li)
    cols = [getColumn(obs, idx) for idx in range(len(obs[0]))]
    for ci, col in enumerate(cols):
        if (all([x == '.' for x in col])):
            ret[1].append(ci)
    return ret

def findGalaxies(obs):
    ret = []
    for li, line in enumerate(obs):
        for ci, c in enumerate(line):
            if c == '#':
                ret.append((len(ret)+1, (li, ci)))
    return ret

def getDist(node1, node2, expansions, expansion=1):
    rowRange = (min(node1[0], node2[0]), max(node1[0], node2[0]))
    colRange = (min(node1[1], node2[1]), max(node1[1], node2[1]))
    rowExp = list(filter(lambda x: x > rowRange[0] and x < rowRange[1], expansions[0]))
    colExp = list(filter(lambda x: x > colRange[0] and x < colRange[1], expansions[1]))
    expandedDistance = len(rowExp)*expansion + len(colExp)*expansion
    return (abs(node1[0]-node2[0]) + abs(node1[1]-node2[1]) + expandedDistance)

with open("input11") as f:
    lines = [line[:-1] for line in f.readlines()]
    exps = findExpansions(lines)
    galaxies = findGalaxies(lines)
    pairs = [(a, b) for idx, a in enumerate(galaxies) for b in galaxies[idx + 1:]]
    getLens = lambda x: [((gid1, gid2), getDist(a,b,exps,expansion=x-1)) for ((gid1, a), (gid2, b)) in pairs]
    print("part1", sum([x[1] for x in getLens(2)]))
    print("part2", sum([x[1] for x in getLens(1000000)]))
