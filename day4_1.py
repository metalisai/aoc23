import re;print(sum(int(2**(len([x for x in m if x in w])-1))for w,m in[[list(re.sub(' +', ' ',x.strip()).split(' '))for x in l.split(':')[1].split('|')]for l in open("4", "r").readlines()]))
