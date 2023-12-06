import re
part1 = False
with open("input6", "r") as f:
    text = re.sub(' +', ' ' if part1 else '', f.read())
    text = re.sub(': ', ':', text)
    parse = lambda idx: [int(x) for x in text.split('\n')[idx].split(':')[1].split(' ')]
    times = parse(0)
    distances = parse(1)
    count = 1
    for time, dist in zip(times, distances):
        ccount = 0
        for i in range(time):
            adist = (time - i) * i
            ccount += 1 if adist > dist else 0
        count *= ccount
    print(count)
