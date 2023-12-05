import portion as P

with open("/home/ttammear/Downloads/input5", "r") as f:
    sections = dict([x.strip().split(':') for x in f.read().split('\n\n')])
    for section in sections.keys():
        sections[section] = [[int(y) for y in x.split(' ')] for x in sections[section].strip().split('\n')]
        
arr = sections['seeds'][0]
ranges1 = list([(x, x+y) for x,y in zip(arr[::2], arr[1::2])])

ranges = [[(x[1], x[1]+x[2], x[0]) for x in sections[y]] for y in sections.keys() if y != "seeds"]

for idx, ranges2 in enumerate(ranges):
    next = []
    totalintr = P.empty()
    totalSrc = P.empty()
    for i1 in ranges1:
        p1 = P.closed(i1[0], i1[1]-1)
        totalSrc = totalSrc | p1
        for i2 in ranges2:
            p2 = P.closed(i2[0], i2[1]-1)
            if p1.overlaps(p2):
                intr = p1&p2 
                totalintr = totalintr | intr
                lower = intr.lower-i2[0]+i2[2]
                upper = intr.upper-i2[0]+i2[2]
                next.append((lower, upper))
    passthrough = (totalSrc - totalintr)
    for mr in passthrough:
        next.append((mr.lower if mr.contains(mr.lower) else mr.lower-1, mr.upper if mr.contains(mr.upper) else mr.upper-1))
    ranges1 = next
print(f"closest location", min([x[0] for x in next]))
