maxcounts = {'red': 12, 'green': 13, 'blue': 14}

sum = 0

with open("/home/ttammear/Downloads/input2", "r") as f:
    lines = f.readlines()
    for line in lines:
        gameValid = True
        
        [label, settext] = line.split(':')
        gameid = int(label.split(' ')[1].strip())
        csets = settext.strip().split(';') # list of sets
        
        maxcounts = {'red': 0, 'green': 0, 'blue': 0}
        
        for cset in csets:
            setValid = True
            
            cset = cset.strip().split(',') # list of samples
            for val in cset:
                val = val.strip()
                color = val.split(' ')[1]
                colorCount = val.split(' ')[0]
                colorCount = int(colorCount)
                #print(f"color \"{color}\" count \"{colorCount}\"")
                if colorCount > maxcounts[color]:
                    maxcounts[color] = colorCount
        #print(f"game {gameid} {maxcounts}")
        power = 1
        for val in maxcounts.values():
            power = power * val
        sum += power
print(f"sum {sum}")
