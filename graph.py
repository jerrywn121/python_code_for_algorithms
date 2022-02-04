class Graph:
    def __init__(self, V):
        self.V = V
        self.E = 0
        self.adj = [[] for _ in range(V)]

    def add_edge(self, v, w):
        self.adj[v].append(w)
        self.adj[w].append(v)
        self.E += 1

    def __str__(self):
        s = f'{self.V} vertices, {self.E} edges\n'
        for v in range(self.V):
            s += str(v) + ': '
            for w in self.adj[v]:
                s += str(w) + ' '
            s += '\n'
        return s


class Digraph:
    def __init__(self, V):
        self.V = V
        self.E = 0
        self.adj = [[] for _ in range(V)]  # should have used a list of bags

    def add_edge(self, v, w):
        self.adj[v].append(w)
        self.E += 1

    def reverse(self):
        R = Digraph(self.V)
        for v in range(self.V):
            for w in self.adj[v]:
                R.add_edge(w, v)
        return R

    def __str__(self):
        s = f'{self.V} vertices, {self.E} edges\n'
        for v in range(self.V):
            s += str(v) + ' -> '
            for w in self.adj[v]:
                s += str(w) + ' '
            s += '\n'
        return s


class SymbolGraph(Graph):
    def __init__(self, keys):
        '''
        For symbol digraph, the implementation is similar
        '''
        self.keys = list(set(keys))
        self.V = len(self.keys)
        self.st = {self.keys[i]: i for i in range(self.V)}  # symbol table
        super().__init__(self.V)

    def index(self, key):
        return self.st.get(key)

    def name(self, i):
        return self.keys[i]

    def add_edge(self, v, w):
        v = self.index(v)
        w = self.index(w)
        self.adj[v].append(w)
        self.adj[w].append(v)
        self.E += 1

    def __str__(self):
        s = f'{self.V} vertices, {self.E} edges\n'
        for v in range(self.V):
            s += str(self.name(v)) + ': '
            for w in self.adj[v]:
                s += str(self.name(w)) + ' '
            s += '\n'
        return s


class Edge:
    def __init__(self, v, w, weight):
        self.v = v
        self.w = w
        self.weight = weight

    def either(self):
        return self.v

    def other(self, vertex):
        if vertex == self.v:
            return self.w
        else:
            return self.v

    def __lt__(self, other):
        return self.weight < other.weight

    def __gt__(self, other):
        return self.weight > other.weight

    def __str__(self):
        return f"{self.v}-{self.w} {self.weight}"


class EdgeWeightedGraph:
    def __init__(self, V):
        self.V = V
        self.adj = [[] for _ in range(V)]
        self.E = 0

    def add_edge(self, e):
        v = e.either()
        w = e.other(v)
        self.adj[v].append(e)
        self.adj[w].append(e)
        self.E += 1

    def edges(self):
        edges = []
        for v in range(self.V):
            for e in self.adj[v]:
                if e.other(v) > v:
                    edges.append(e)
        return edges

    def __str__(self):
        s = f'{self.V} vertices, {self.E} edges\n'
        for v in range(self.V):
            s += f'{v}: '
            for e in self.adj[v]:
                s += f'{e}, '
            s += '\n'
        return s.strip()


class DirectedEdge:
    def __init__(self, v, w, weight):
        self.v = v
        self.w = w
        self.weight = weight

    def from_(self):
        return self.v

    def to(self):
        return self.w

    def __eq__(self, other):
        return self.weight == other.weight

    def __gt__(self, other):
        return self.weight > other.weight

    def __str__(self):
        return f"{self.v}->{self.w} {self.weight}"


class EdgeWeightedDigraph:
    def __init__(self, V):
        self.V = V
        self.adj = [[] for _ in range(V)]
        self.E = 0

    def add_edge(self, e):
        self.adj[e.from_()].append(e)
        self.E += 1

    def edges(self):
        edges = []
        for v in range(self.V):
            for e in self.adj[v]:
                edges.append(e)
        return edges

    def __str__(self):
        s = f'{self.V} vertices, {self.E} edges\n'
        for v in range(self.V):
            s += f'{v}: '
            for e in self.adj[v]:
                s += f'{e}, '
            s += '\n'
        return s.strip()
