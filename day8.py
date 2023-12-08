import math

part1 = False

with open("input8") as f:
    lines = [line.replace('\n','') for line in f.readlines()]
    instruction = lines[0]
    nodes = {x[0]:(x[1][1:4],x[1][6:9]) for x in (node.split(' = ') for node in lines[2:])}
    
    check = lambda x: x == "ZZZ" if part1 else x[2] == "Z"
        
    def traverse(node, instructions):
        idx = 0
        while not check(node):
            leftOrRight = 0 if instructions[idx%len(instructions)] == "L" else 1
            node = nodes[node][leftOrRight]
            idx += 1
        return idx
    
    scheck = (lambda x: x == "AAA") if part1 else (lambda x: x[2] == "A")
    starts = list(filter(scheck, list(nodes.keys())))
    factors = []
    for idx, start in enumerate(starts):
        res = traverse(start, instruction)
        factors.append(res)
    print(factors)
    print(math.lcm(*factors))
