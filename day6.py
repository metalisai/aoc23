import re
import math
part1 = False
with open("input6", "r") as f:
    text = re.sub(' +', ' ' if part1 else '', f.read())
    text = re.sub(': ', ':', text)
    parse = lambda idx: [int(x) for x in text.split('\n')[idx].split(':')[1].split(' ')]
    times = parse(0)
    distances = parse(1)
    count = 1
    for time, dist in zip(times, distances):
        r1 = (time + math.sqrt(time*time-4*dist))/2.0
        r2 = (time - math.sqrt(time*time-4*dist))/2.0
        r1 = int(math.ceil(r1)) if r2 > r1 else int(math.floor(r1))
        r2 = int(math.ceil(r2)) if r1 > r2 else int(math.floor(r2))       
        if (time-r1)*r1 == dist:
            r1 = r1 + math.copysign(1, r2-r1)
        if (time-r2)*r2 == dist:
            r2 = r2 + math.copysign(1, r1-r2)
        ans = abs(r1-r2)+1
        count *= ans
    print(count)
