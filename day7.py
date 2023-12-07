from collections import Counter

part1 = True
cardStrength = {'2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, 'T': 9, 'Q': 11, 'K': 12, 'A': 13, 'J': 10 if part1 else 0}

def getStrengthClass(hand):
    c = Counter(hand).most_common()
    mc = c[0][1]
    
    if not part1:
        try:
            mmax = max(filter(lambda x: x[0] != 'J', c), key=lambda x: 100*x[1]+cardStrength[x[0]])
            repc = mmax[0]
        except:
            if c[0][1] == 5 and c[0][0] == 'J':
                repc = 'A'
            else:
                repc = c[0][0]    
        hand2 = hand.replace('J', repc)
        if hand != hand2:
            return getStrengthClass(hand2)
        
    if mc != 5:
        sc = c[1][1]  
    
    if mc == 5:
        return 7
    elif mc == 4:
        return 6
    elif mc == 3 and sc == 2:
        return 5
    elif mc == 3:
        return 4
    elif mc == 2 and sc == 2:
        return 3
    elif mc == 2:
        return 2
    else:
        return 1
    
def key(hand):
    return sum([cardStrength[d]<<(4*i) for i,d in enumerate(hand[::-1])]) + (getStrengthClass(hand) << 20)

with open("input7", "r") as f:
    hands = [(hand, int(bid[:-1])) for hand, bid in (line.split(' ') for line in f.readlines())]
    hands = sorted(hands, key=lambda x: key(x[0]))
    winnings = sum([(i+1)*x[1] for i,x in enumerate(hands)])
    print(winnings)
