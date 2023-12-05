import re

with open("input", "r") as f:
    sections = dict([x.strip().split(':') for x in f.read().split('\n\n')])
    for section in sections.keys():
        sections[section] = [[int(y) for y in x.split(' ')] for x in sections[section].strip().split('\n')]

def edges(section, mappings):
    ret = []
    for ms in mappings:
        count = ms[2]
        fun = (ms[1], ms[1]+ms[2], ms[0])
        ret.append(fun)
    return ret

def destName(section):
    return section.split(' ')[0].split('-')[2]

def traverse(node):
    global locations
    branches = [x for x in sections.keys() if re.match(f'{node[1]}-.+', x)]
    if len(branches) == 0:
        return
    branch = branches[0]
    nedges = edges(branch, sections[branch])
    
    destination = None
    for edgeRange in nedges:
        if node[0] >= edgeRange[0] and node[0] < edgeRange[1]:
            destination = (node[0]-edgeRange[0]+edgeRange[2], destName(branch))
            break
    if destination is None:
        destination = (node[0], destName(branch))
    
    if destination[1] == 'location':
        locations.append(destination)
    traverse(destination)

locations = []
for seed in sections['seeds'][0]:
    traverse((seed, 'seed'))

print(f'(Part1) closest location is {min(locations, key=lambda x: x[0])}')
