import re

lines = []

with open("/home/ttammear/Downloads/input3", "r") as f:
    for line in f.readlines():
        lines.append(line)

exp = re.compile("[0-9]{1,3}")
numbers = {}

def getChar(row, col):
    if row < 0 or row >= len(lines) or col < 0 or col >= len(lines[0])-1:
        return '.'
    return lines[row][col]

def findNumber(row, col):
    for span in numbers.keys():
        if row == span[0] and col >= span[1] and col < span[2]:
            return span

def getAdjacentNumbers(row, col):
    ret = []
    for i in range(col-1, col+2):
        for j in range(row-1, row+2):
            if getChar(j, i).isnumeric():
                ret.append(findNumber(j, i))
    return list(set(ret))

parts = set()

for row, line in enumerate(lines):
    for match in exp.finditer(line):
        numbers[(row, match.start(), match.end())] = int(match.group())
            
ratiosum = 0
for row, line in enumerate(lines):
    for col, c in enumerate(line):
        if c == '*':
            nrs = getAdjacentNumbers(row, col)
            if len(nrs) == 2:
                ratiosum += numbers[nrs[0]]*numbers[nrs[1]]
                
print(f"ratio sum {ratiosum}")
