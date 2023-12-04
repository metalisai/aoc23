import re
score = 0
with open("/home/ttammear/Downloads/input4", "r") as f:
    for line in f.readlines():
        (winning, mine) = [list(re.sub('\s+', ' ', x.strip()).split(' ')) for x in line.split(':')[1].split('|')]
        score += int(2 ** (len([x for x in mine if x in winning])-1))
print(score)
