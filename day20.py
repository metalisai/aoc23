import re
import graphviz
import math

hcount = 0
lcount = 0

def process(moduleDict, value, name, src):
    global lcount, hcount
    module = moduleDict[name]

    if not value:
        lcount += 1
    else:
        hcount += 1

    ret = []
    
    def outputPulse(outvalue):
        for cmod in module[1]:
            ret.append((outvalue, cmod, module[0][1]))
    
    mtype = module[0][0]
    if mtype == "%":
        if not value:
            module[2] = not module[2]
            outputPulse(module[2])
    elif mtype == "&":
        module[2][src] = value
        if all(module[2].values()):
            outputPulse(False)
        else:
            outputPulse(True)
    elif mtype == "":
        outputPulse(value)
    elif mtype == "rx":
        if not value:
            return None
        outputPulse(value)
    return ret

with open("input20") as f:
    lines = f.read().splitlines()
    modules = []
    for module in lines:
        mid, targets = module.split(' -> ')
        mtype, mname = re.findall('([&%]?)([A-z]*)', mid)[0]
        targets = [x.strip() for x in targets.split(',')]
        modules.append([(mtype, mname), targets, False if mtype == '%' else {}])
        
    for conj in (mod for mod in modules if mod[0][0] == '&'):
        for module in modules:
            if conj[0][1] in module[1]:
                conj[2][module[0][1]] = False
        
    moduleDict = {m[0][1]: m for m in modules}

    for mod in modules:
        for target in mod[1]:
            if target not in moduleDict:
                moduleDict[target] = [('rx', target), [], None, []]

    cyclers = []
    cycles = {}
    for mod in moduleDict['broadcaster'][1]:
        for l2 in moduleDict[mod][1]:
            if moduleDict[l2][0][0] == '&':
                cyclers.append(l2)
                cycles[l2] = set([])

    for i in range(0xDEAD):
        signals = [(False, "broadcaster", "button")]
        while len(signals) > 0:
            signal = signals.pop(0)
            if signal[2] in cyclers and signal[0] == False:
                cycles[signal[2]].add(i)
            result = process(moduleDict, signal[0], signal[1], signal[2])
            if result is None: # how naive
                print("part2 ", i)
                exit()
                break
            else:
                signals.extend(result)

        if i == 1000-1:
            part1 = lcount * hcount
            print("part1", part1)

    factors = [sorted(list(value))[-1]-sorted(list(value))[-2] for value in cycles.values()]
    print("part2", math.lcm(*factors))

    exit()

    dot = graphviz.Digraph('round-table', comment="What")
    for module in moduleDict.keys():
        m = moduleDict[module]
        dot.node(m[0][1], m[0][1] + f"({m[0][0]})")
    for module in moduleDict.keys():
        m = moduleDict[module]
        for me in m[1]:
            m2 = moduleDict[me]
            dot.edge(m[0][1], m2[0][1])
    dot.render(directory='gviz')
