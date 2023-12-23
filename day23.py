offsets = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def find(mmap, start=True):
    for ci, c in enumerate(mmap[0] if start else mmap[len(mmap)-1]):
        if c == ".":
            return (0 if start else len(mmap)-1, ci)
    return (-1, -1)

def findNodes(mmap):
    start = find(mmap, start=True)
    end = find(mmap, start=False)
    nodes = [start, end]
    for i, line in enumerate(mmap):
        for ci, c in enumerate(line):
            if c == '#':
                continue
            edges = []
            for o in offsets:
                nextN = (o[0]+i, o[1]+ci)
                if nextN[0] < 0 or nextN[0] == len(mmap) or nextN[1] < 0 or nextN[1] == len(mmap[0]):
                    continue
                if mmap[nextN[0]][nextN[1]] == '#':
                    continue
                edges.append(nextN)
            if len(edges) > 2:
                nodes.append((i, ci))
    return nodes

def dfs_(mmap, node, start, end, dist, visited, nodes):
    if node[0] < 0 or node[0] >= len(mmap) or node in visited:
        return -99999
    curC = mmap[node[0]][node[1]]
    if curC == "#":
        return -99999
    if node == end:
        return 0
    if node != start and node in nodes:
        return -99999
    visited.add(node)
    dists = []
    for o in offsets:
        nextN = (o[0] + node[0], o[1] + node[1])
        dists.append(dfs_(mmap, nextN, start, end, dist+1, visited, nodes))
    return max(dists) + 1

def dfs(mmap, pair, nodes):
    node1, node2 = pair
    visited = set()
    return dfs_(mmap, node1, node1, node2, 0, visited, nodes)

def findDistances(mmap, nodes):
    pairs = [(idx, idx+bi+1) for idx, a in enumerate(nodes) for bi, b in enumerate(nodes[idx + 1:])]
    edges = {}
    for n1, n2 in pairs:
        dist = dfs(mmap, (nodes[n1], nodes[n2]), nodes)
        if dist < 0:
            continue
        if n1 not in edges:
            edges[n1] = []
        if n2 not in edges:
            edges[n2] = []
        edges[n1].append((n2, dist))
        edges[n2].append((n1, dist))
    visited = []
    def traverse(node, dist):
        if node == 1:
            return 0
        if node in visited:
            return -99999
        visited.append(node)
        costList = []
        for idx, cost in edges[node]:
            res = traverse(idx, dist+cost)
            costList.append((res, cost))
        visited.pop()
        bestNode = max(costList, key=lambda x: x[0]+x[1])
        return sum(bestNode)
    return traverse(0, 0)

# This smells like 'magic' input.
with open("input23") as f:
    data = [[c for c in line] for line in f.read().splitlines()]
    nodes = findNodes(data)
    print("part2", findDistances(data, nodes))
