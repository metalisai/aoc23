import re
cards = {}
mynrs = []
unwrapped = []
with open("/home/ttammear/Downloads/input4", "r") as f:
    for idx, line in enumerate(f.readlines()):
        (winning, mine) = [list(re.sub('\s+', ' ', x.strip()).split(' ')) for x in line.split(':')[1].split('|')]
        card = (idx+1, winning, mine)
        cards[idx+1] = card
        mynrs.append(int(idx+1))   

def unwrap(cardId, test="?"):
    unwrapped.append(cardId)
    card = cards[cardId]
    matches = len([x for x in card[2] if x in card[1]])
    [unwrap(x) for x in range(cardId+1, cardId+1+matches)]

for card in mynrs:
    unwrap(card)
    
print(len(unwrapped))
