from stack_queue import LinkedListStack, LinkedListQueue


class Graph:
    def __init__(self, V):
        self.V = V
        self.E = 0
        self.adj = [[] for _ in range(V)]  # should have used a list of bags

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


class DFS:
    def __init__(self, G, s):
        self.G = G
        self.s = s
        self.marked = [False] * G.V
        self.edge_to = [None] * G.V
        self.count = 0  # how many vertices are connected to s
        self.dfs(s)

    def dfs(self, v):
        '''
        mark v and visit all unmarked vertices adjacent to v
        in time proportional to the sum of the degrees of all vertices connected to s
        '''
        self.marked[v] = True
        self.count += 1
        for w in self.G.adj[v]:
            if not self.marked[w]:
                self.edge_to[w] = v
                self.dfs(w)

    def has_path_to(self, v):
        return self.marked[v]

    def path_to(self, v):
        if not self.has_path_to(v):
            return None
        path = LinkedListStack()
        while v != self.s:
            path.push(v)
            v = self.edge_to[v]
        path.push(v)
        return path

    def paths(self):
        '''
        print paths from s
        '''
        for v in range(self.G.V):
            if self.has_path_to(v):
                print(self.path_to(v))


class BFS:
    def __init__(self, G, s):
        self.G = G
        self.s = s
        self.marked = [False] * G.V
        self.edge_to = [False] * G.V
        self.bfs(s)

    def bfs(self, s):
        '''
        dequeue the item from the queue and mark it, and
        put on queue all the unmarked vertices adjacent to it
        in time proportional to O(E + V) = O(1 + e) * O(V)
        '''
        q = LinkedListQueue()
        q.enqueue(self.s)
        self.marked[s] = True
        while not q.is_empty():
            v = q.dequeue()
            for w in self.G.adj[v]:
                if not self.marked[w]:
                    q.enqueue(w)
                    self.edge_to[w] = v
                    self.marked[w] = True

    def has_path_to(self, v):
        return self.marked[v]

    def path_to(self, v):
        if not self.has_path_to(v):
            return None
        path = LinkedListStack()
        while v != self.s:
            path.push(v)
            v = self.edge_to[v]
        path.push(v)
        return path

    def paths(self):
        '''
        print paths from s
        '''
        for v in range(self.G.V):
            if self.has_path_to(v):
                print(self.path_to(v))


class Cycle:
    def __init__(self, G):
        self.G = G
        self.marked = [False] * G.V
        self.edge_to = [0] * G.V
        self.has_cycle = False
        for s in range(G.V):
            if not self.marked[s]:
                self.dfs(s, s)

    def dfs(self, v, u):
        '''
        the argument u indicates that dfs(v) is called in dfs(u)
        '''
        self.marked[v] = True
        for w in self.G.adj[v]:
            if not self.marked[w]:
                self.edge_to[w] = v
                self.dfs(w, v)
            elif w != u:
                self.has_cycle = True
                return


class DirectedCycle:
    def __init__(self, G):
        self.G = G
        self.marked = [False] * G.V
        self.cycle = LinkedListStack()
        self.edge_to = [0] * G.V
        self.on_stack = [False] * G.V
        for s in range(G.V):
            if not self.marked[s]:
                self.dfs(s)

    def dfs(self, v):
        self.on_stack[v] = True
        self.marked[v] = True
        for w in self.G.adj[v]:
            if self.has_cycle():
                return
            if not self.marked[w]:
                self.edge_to[w] = v
                self.dfs(w)
            elif self.on_stack[w]:
                '''
                if w is onstack, which means that it must be marked,
                there must a directed path from w to v as we are now calling
                function dfs(v). Hence, there is a directed cycle (w->v, v->w)
                '''
                x = v
                while x != w:
                    self.cycle.push(x)
                    x = self.edge_to[x]
                self.cycle.push(w)
                self.cycle.push(v)
        self.on_stack[v] = False

    def has_cycle(self):
        return not self.cycle.is_empty()


class DepthFirstOrder:
    def __init__(self, G):
        self.G = G
        self.reverse_post = LinkedListStack()
        self.marked = [False] * G.V
        for s in range(G.V):
            if not self.marked[s]:
                self.dfs(s)
    
    def dfs(self, v):
        self.marked[v] = True
        for w in self.G.adj[v]:
            if not self.marked[w]:
                self.dfs(w)
        self.reverse_post.push(v)


class TopologicalSort:
    def __init__(self, G):
        self.order = None
        self.G = G
        self.directed_cycle = DirectedCycle(G)
        if not self.directed_cycle.has_cycle():
            self.order = DepthFirstOrder(G).reverse_post

    def is_dag(self):
        return self.order is not None


class ConnectedComponent:
    def __init__(self, G):
        self.G = G
        self.count = 0
        self.ID = [0] * G.V
        self.marked = [False] * G.V
        for v in range(G.V):
            if not self.marked[v]:
                self.dfs(G, v)
                self.count += 1

    def dfs(self, G, v):
        self.marked[v] = True
        self.ID[v] = self.count
        for w in G.adj[v]:
            if not self.marked[w]:
                self.dfs(G, w)

    def connected(self, v, w):
        return self.ID[v] == self.ID[w]


class StronglyConnectedComponent:
    def __init__(self, G):
        self.G = G
        self.count = 0
        self.ID = [0] * G.V
        self.marked = [False] * G.V
        reverse_post = DepthFirstOrder(G.reverse()).reverse_post.tolist()
        for v in reverse_post:
            if not self.marked[v]:
                self.dfs(G, v)
                self.count += 1

    def dfs(self, G, v):
        self.marked[v] = True
        self.ID[v] = self.count
        for w in G.adj[v]:
            if not self.marked[w]:
                self.dfs(G, w)

    def connected(self, v, w):
        return self.ID[v] == self.ID[w]


# ----- client code -----
def CC(G):
    cc = ConnectedComponent(G)
    components = [[] for _ in range(cc.count)]
    for v in range(G.V):
        components[cc.ID[v]].append(v)
    for i, x in enumerate(components):
        print(f"Component {i}: {x}")


def SCC(G):
    scc = StronglyConnectedComponent(G)
    components = [[] for _ in range(scc.count)]
    for v in range(G.V):
        components[scc.ID[v]].append(v)
    for i, x in enumerate(components):
        print(f"Component {i}: {x}")
