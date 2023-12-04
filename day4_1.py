import re
print(sum(int(2**(len([x for x in m if x in w])-1)) for w, m in [[list(re.sub('\s+', ' ', x.strip()).split(' ')) for x in line.split(':')[1].split('|')] for line in open("4", "r").readlines()]))
