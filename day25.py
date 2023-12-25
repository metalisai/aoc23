import random

class Machinery:
    def __init__(self, nodes=None):
        self.edges = []
        self.vertices = []
        if nodes is not None:
            vs = set()
            for line in nodes:
                v = line[0][0]
                vs.add(v)
                for target in line[1]:
                    self.edges.append((v, target))
                    vs.add(target)
            self.vertices = list(vs)
    def getEdges(self):
        return self.edges
    def contractEdge(self, idx):
        edges = self.edges
        vertices = self.vertices 
        src, dst = edges[idx]
        self.edges = list(filter(lambda x: (x[0]!=src and x[1]!=src)or(x[1]!=dst and x[0]!=dst), self.edges))
        edges = self.edges
        srcIdx = -9999999
        for vi,v in enumerate(vertices):
            if v == src:
                vertices[vi] = f"{src},{dst}"
                srcIdx = vi
                break
        if srcIdx < 0:
            raise Exception(f"{src} not found")
        for ei,_ in enumerate(edges):
            if edges[ei][0] == dst or edges[ei][0] == src:
                edges[ei] = (vertices[srcIdx], edges[ei][1])
            if edges[ei][1] == dst or edges[ei][1] == src:
                edges[ei] = (edges[ei][0], vertices[srcIdx])
        vertices.remove(dst)
    def getVertices(self):
        return self.vertices
    def copy(self):
        ret = Machinery()
        ret.vertices = self.vertices.copy()
        ret.edges = self.edges.copy()
        return ret

# Think there's a bug somewhere... Oh well, just pray to RNGesus
while True:
    with open("input25") as f:
        lines = f.read().splitlines()
        lines = [[node.split(' ') for node in line.split(': ')] for line in lines]
        machinery = Machinery(lines)

        while len(machinery.getVertices()) > 2:
            ei = random.randrange(len(machinery.getEdges()))
            machinery.contractEdge(ei)

        v1, v2 = machinery.getVertices()
        l1 = len(v1.split(','))
        l2 = len(v2.split(','))
        if len(machinery.getEdges()) == 3:
            print("part1", l1*l2)
            break
            
# as someone who never did stuff like this before, was fun
# some problems took way too long (like 21, 12 if you don't know DP, maybe 5 and 10)
#   (for 21 I'm not sure if I would've reached a solution without hints and without losing my mind)
# but I can see how someone more experienced would get them all in an hour or two (excluding professionals)
