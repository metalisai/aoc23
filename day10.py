edges = {
    '|': [(-1,0),(1,0)],
    '-': [(0,1),(0,-1)],
    'L': [(-1,0),(0,1)],
    'J': [(-1,0),(0,-1)],
    '7': [(1,0),(0,-1)],
    'F': [(1,0),(0,1)],
    '.': [],
    'S': [(0,1),(0,-1),(1,0),(-1,0)],
}

def find(nodes, value):
    for i in range(len(nodes)):
        for j in range(len(nodes[0])):
            if nodes[i][j] == value:
                return (i,j)
            
def countChanges(xs):
    prev = 0
    count = 0
    for x in xs:
        if x != prev:
            count += 1
        prev = x
    return count
            
def countInternal(nodes, path, connected):
    strip = [pair for pair in zip(path, path[1:])]
    count = 0
    for idx, _ in enumerate(nodes):
        intersections = []
        for seg in strip:
            row1 = seg[0][0]
            row2 = seg[1][0]
            if (row1 == idx or row2 == idx) and row1 != row2:
                intersections.append((seg[0][1], seg[0][0]-seg[1][0]))
        intersections.sort()
        for ci in range(len(nodes[0])):
            smaller = list(filter(lambda x: x[0] < ci, intersections))
            changes = countChanges([x[1] for x in smaller])
            if (changes&1) == 1 and (idx, ci) not in path:
                count += 1
    print("Part2", count)

def findLoop(nodes, start):
    def getC(coord):
        return nodes[coord[0]][coord[1]]
    
    def connected(node1, node2):
        edges1 = [(e[0]+node1[0],e[1]+node1[1]) for e in edges[getC(node1)]]
        edges2 = [(e[0]+node2[0],e[1]+node2[1]) for e in edges[getC(node2)]]
        return node1 in edges2 and node2 in edges1
    
    def backtrack(node):
        ret = [node]
        while getC(node) != 'S':
            node = cameFrom[node]
            ret.append(node)
        return ret
    
    open = [start]
    cameFrom = {}
    gs = {start: 0}
    cur = None
    started = False
    # no do while, pain
    prev = None
    while cur != start or not started:
        if len(open) == 0:
            break
        
        pairs = [(a, b) for idx, a in enumerate(open) for b in open[idx + 1:]]
        conP = [connected(a, b) for a,b in pairs]
        if any(conP):
            matching = pairs[conP.index(True)]
            print("FOUND PATH\nPart1", max(gs[matching[0]], gs[matching[1]]))
            countInternal(nodes, backtrack(matching[0])[::-1]+backtrack(matching[1]), connected)
            break
        
        cur = min(open, key=lambda x: gs[x])
        open.remove(cur)
        if cur != start:
            started = True
        for edge in edges[getC(cur)]:
            next = (edge[0]+cur[0],edge[1]+cur[1])
            
            if next in cameFrom and cameFrom[next] == cur or next in gs or not connected(cur, next):
                continue
            g = gs[cur]+1
            if next not in gs or g < gs[next]:
                gs[next] = g
            cameFrom[next] = cur
            open.append(next)

with open("input10") as f:
    mymap = []
    for line in f.readlines():
        cs = ['.']
        nodes = []
        for c in line[:-1]:
            #print(c)
            cs.append(c)
        cs.append('.')
        mymap.append(cs)
    emptyLine = ['.']*len(mymap[0])
    mymap.insert(0, emptyLine)
    mymap.append(emptyLine)
    start = find(mymap, 'S')
    findLoop(mymap, start)
