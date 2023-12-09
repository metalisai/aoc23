part1 = False
def down(nrs):
    pairs = zip(nrs[::1], nrs[1::1])
    return [pair[1] - pair[0] for pair in pairs]

def extrapolate(nrs, end = True):
    levels = [nrs]
    while not all([x == 0 for x in levels[-1]]):
        levels.append(down(levels[-1]))
    if end:
        levels[-1].append(0)
        for prev, level in zip(levels[::-1], levels[-2::-1]):
            level.append(level[-1]+prev[-1])
    else:
        levels[-1].insert(0, 0)
        for prev, level in zip(levels[::-1], levels[-2::-1]):
            level.insert(0, level[0]-prev[0])     
    return levels[0][-1] if end else levels[0][0]

with open("input9") as f:
    ans = [extrapolate([int(x) for x in line.split(" ")], end=part1) for line in f.readlines()]
    print(sum(ans))
