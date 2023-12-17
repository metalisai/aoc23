import queue

def dirs(curDir, canTurn):
    if canTurn:
        return [(curDir[1], curDir[0]), (-curDir[1], -curDir[0]), curDir]
    else:
        return [curDir]

# well, it was supposed to be A*, but it's Dijkstra's cause it was good enough
def statefulAstar(nodes, start, goal, direction, maxConsecutive, minConsecutive):
    consecutive = 0
    startNode = (start, direction, consecutive)
    openSet = list([startNode])
    
    openSet = queue.PriorityQueue()
    openSet.put((0, startNode))
    
    gScores = {startNode: 0}
    cameFrom = {}
    while not openSet.empty():
        cur = openSet.get()[1]
        curNode = cur[0]
        if curNode == goal and cur[2] >= minConsecutive-1:
            return gScores[cur]
        curDir = cur[1]
        for nextDir in dirs(curDir, cur[2] >= minConsecutive-1):
            nextNode = (curNode[0]+nextDir[0], curNode[1]+nextDir[1])
            if nextNode[0] < 0 or nextNode[0] >= len(nodes) or nextNode[1] < 0 or nextNode[1] >= len(nodes[0]):
                continue
            nextConsecutive = 0 if nextDir != curDir else cur[2] + 1
            if nextConsecutive >= maxConsecutive:
                continue
            cost = nodes[nextNode[0]][nextNode[1]]
            totalCost = gScores[cur] + cost
            nextn = (nextNode, nextDir, nextConsecutive)
            if nextn in gScores and totalCost >= gScores[nextn]:
                continue
            gScores[nextn] = totalCost
            cameFrom[nextn] = cur
            openSet.put((totalCost, nextn))
    return -1

with open("input17") as f:
    lines = [[int(c) for c in line[:-1]] for line in f.readlines()]
    goal = (len(lines)-1, len(lines[0])-1)
    start = (0, 0)
    direction = (0, 1) # right
    part1 = statefulAstar(lines, start, goal, direction, 3, 0)
    part2 = statefulAstar(lines, start, goal, direction, 10, 4)
    print(f"part1: {part1}\npart2: {part2}")
