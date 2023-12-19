import re
import portion as P

def getPart(line):
    def getValue(value):
        l, v = value.split('=')
        return (l, int(v))
    values = [getValue(value) for value in line[1:-1].split(',')]
    values = {v[0]: v[1] for v in values}
    return {"values": values, "workflow": "in"}
    
def getWorkflow(line):
    exp = "([9-z]+)\{(.+)\}"
    label, rules = re.findall(exp, line)[0]
    rules = rules.split(',')
    prules = []
    for rule in rules:
        try:
            condition, action = rule.split(':')
        except:
            condition = None
            action = rule
        if condition is not None:
            condition = re.findall("([9-z]+)([<>])([0-9]+)", condition)[0]
            condition = (condition[0], condition[1], int(condition[2]))
        prules.append((condition, action))
    return {"name": label, "rules": prules}

def traverse(workflows, node, remainingIntervals, removed, depth=0):
    spaces = ''.join([' ']*depth*2)
    if node == 'R' or node == 'A':
        if node == 'R':
            removed.append(remainingIntervals.copy())
        return
    rules = workflows[node]
    for condition, nextwf in rules:
        newIntervals = remainingIntervals.copy()
        if condition != None:
            if condition[1] == '<':
                condp = P.closed(0, condition[2]-1)
            else:
                condp = P.closed(condition[2]+1, 999999)
            newIntervals[condition[0]] = newIntervals[condition[0]] & condp
            remainingIntervals[condition[0]] = remainingIntervals[condition[0]] - condp
        traverse(workflows, nextwf, newIntervals, removed, depth+1)
        
with open("input19") as f:
    data = f.read()
    rules, parts = data.split("\n\n")
    rules = rules.split('\n')
    parts = [x for x in parts.split('\n') if x != '']
    
    workflows = [getWorkflow(rule) for rule in rules]
    workflows = {wf["name"]: wf["rules"] for wf in workflows}
    parts = [getPart(part) for part in parts]
    
    accepted = []
    rejected = []
    
    while len(parts) > 0:
        part = parts.pop()
        workflow = workflows[part["workflow"]]
        for condition, nextWf in workflow:
            if condition == None:
                part["workflow"] = nextWf
                break
            else:
                partValue = part["values"][condition[0]]
                if condition[1] == '<' and partValue < condition[2]:
                    part["workflow"] = nextWf
                    break
                elif condition[1] == '>' and partValue > condition[2]:
                    part["workflow"] = nextWf
                    break       
        match part["workflow"]:
            case "R":
                rejected.append(part)
            case "A":
                accepted.append(part)
            case _:
                parts.append(part)
    
    print("part1", sum(val for part in accepted for val in part["values"].values()))
    
    x = P.closed(1, 4000)
    m = P.closed(1, 4000)
    a = P.closed(1, 4000)
    s = P.closed(1, 4000)

    removed = []
    
    traverse(workflows, 'in', { "x": x, "m": m, "a": a, "s": s }, removed)
    
    totalCombinations = 4000*4000*4000*4000
    for area in removed:
        counts = []
        for k in area.keys():
            try:
                upper = area[k].upper if area[k].contains(area[k].upper) else area[k].upper - 1
                lower = area[k].lower if area[k].contains(area[k].lower) else area[k].lower + 1
                counts.append(max(upper-lower+1, 0))
            except:
                counts.append(0)
                pass
        product = 1
        for x in counts:
            product *= x
        totalCombinations -= product
    print("part2", totalCombinations)
