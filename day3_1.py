import re

lines = []

with open("/home/ttammear/Downloads/input3", "r") as f:
    for line in f.readlines():
        lines.append(line)

exp = re.compile("[0-9]{1,3}")

def getChar(row, col):
    if row < 0 or row >= len(lines) or col < 0 or col >= len(lines[0])-1:
        return '.'
    return lines[row][col]

def nextToPart(row, spanStart, spanEnd):
    for i in range(spanStart-1, spanEnd+1): #column
        for j in range(row-1, row+2):
            if j == row and i >= spanStart and i < spanEnd:
                continue
            c = getChar(j, i)
            if c != '.' and not c.isnumeric():
                return True
    return False

sum = 0

for row, line in enumerate(lines):
    for match in exp.finditer(line):
        isNextToPart = nextToPart(row, match.start(), match.end())
        if isNextToPart:
            sum += int(match.group())
        
print(f"sum is {sum}")
