from stack_queue import Stack, IndexPriorityQueueMin
from graph import DirectedEdge, EdgeWeightedDigraph


class ShortestPath:
    def __init__(self, G, s):
        self.dist_to = [float("inf")] * G.V
        self.dist_to[s] = 0.
        self.edge_to = [None] * G.V

    def has_path_to(self, v):
        return self.dist_to[v] < float("inf") and self.edge_to[v] is not None

    def path_to(self, v):
        if not self.has_path_to(v):
            return None
        path = Stack()
        e = self.edge_to[v]
        while e is not None:
            path.push(e)
            e = self.edge_to[e.from_()]
        return path

    def _check(self, G, s):
        # check that edge weights are non-negative
        for e in G.edges():
            if e.weight < 0:
                print("negative edge weight detected")
                return False

        # check that dist_to[v] and edge_to[v] are consistent
        if self.dist_to[s] != 0 or self.edge_to[s] is not None:
            print("dist_to[s] and edge_to[s] inconsistent")
            return False
        for v in range(G.V):
            if v == s:
                continue
            if self.edge_to[v] is None and self.dist_to[v] < float("inf"):
                print("dist_to[] and edge_to[] inconsistent")
                return False
        for v in range(G.V):
            path = self.path_to(v)
            if path is not None:
                if not sum([e.weight for e in path.tolist()]) == self.dist_to[v]:
                    print("dist_to[] and edge_to[] inconsistent")
                    return False
        # check that all edges e = v->w satisfy dist_to[w] <= dist_to[v] + e.weight
        for v in range(G.V):
            for e in G.adj[v]:
                w = e.to()
                if self.dist_to[w] > self.dist_to[v] + e.weight:
                    print(f"edge {e} not relaxed")
                    return False
        # check that all edges e = v->w on SPT satisfy dist_to[w] == dist_to[v] + e.weight
        for w in range(G.V):
            e = self.edge_to[w]
            if e is None:
                continue
            v = e.from_()
            if w != e.to():
                return False
            if self.dist_to[w] != self.dist_to[v] + e.weight:
                print(f"edge {e} on shortest path not tight")
                return False
        return True


class DijkstraSP(ShortestPath):
    def __init__(self, G, s):
        super().__init__(G, s)
        self.pq = IndexPriorityQueueMin(G.V)
        self.pq.insert(s, 0.)
        while not self.pq.is_empty():
            v = self.pq.del_min()
            for e in G.adj[v]:
                self._relax(e)

    def _relax(self, e):
        '''
        relax edge e and add to pq / update non-tree vertex
        '''
        v = e.from_()
        w = e.to()
        if self.dist_to[w] > self.dist_to[v] + e.weight:
            self.dist_to[w] = self.dist_to[v] + e.weight
            self.edge_to[w] = e
            # update pq
            if self.pq.contains(w):
                self.pq.decrease_key(w, self.dist_to[w])
            else:
                self.pq.insert(w, self.dist_to[w])


class AcyclicSP(ShortestPath):
    def __init__(self, G, s):
        super().__init__(G, s)
        for v in self._topological(G):
            for e in G.adj[v]:
                self._relax(e)

    def _relax(self, e):
        '''
        relax edge e and add to pq / update non-tree vertex
        '''
        v = e.from_()
        w = e.to()
        if self.dist_to[w] > self.dist_to[v] + e.weight:
            self.dist_to[w] = self.dist_to[v] + e.weight
            self.edge_to[w] = e

    def _topological(self, G):
        marked = [False] * G.V
        order = Stack()
        for s in range(G.V):
            if not marked[s]:
                self._dfs(G, s, marked, order)
        return order.tolist()

    def _dfs(self, G, v, marked, order):
        marked[v] = True
        for e in G.adj[v]:
            w = e.to()
            if not marked[w]:
                self._dfs(G, w, marked, order)
        order.push(v)


class AcyclicLP:
    def __init__(self, G, s):
        self.dist_to = [float("-inf")] * G.V
        self.dist_to[s] = 0.
        self.edge_to = [None] * G.V
        for v in self._topological(G):
            for e in G.adj[v]:
                self._relax(e)

    def _relax(self, e):
        '''
        relax edge e and add to pq / update non-tree vertex
        '''
        v = e.from_()
        w = e.to()
        if self.dist_to[w] < self.dist_to[v] + e.weight:
            self.dist_to[w] = self.dist_to[v] + e.weight
            self.edge_to[w] = e

    def _topological(self, G):
        marked = [False] * G.V
        order = Stack()
        for s in range(G.V):
            if not marked[s]:
                self._dfs(G, s, marked, order)
        return order.tolist()

    def _dfs(self, G, v, marked, order):
        marked[v] = True
        for e in G.adj[v]:
            w = e.to()
            if not marked[w]:
                self._dfs(G, w, marked, order)
        order.push(v)

    def has_path_to(self, v):
        return self.dist_to[v] > float("-inf") and self.edge_to[v] is not None

    def path_to(self, v):
        if not self.has_path_to(v):
            return None
        path = Stack()
        e = self.edge_to[v]
        while e is not None:
            path.push(e)
            e = self.edge_to[e.from_()]
        return path


class CriticalPathMethod:
    '''
    Critical path method for parallel precedence-constrained job scheduling
    '''
    def __init__(self, duration, precedence):
        '''
        n is the number of jobs
        '''
        n = len(duration)
        s = 2 * n
        t = 2 * n + 1
        self.n = n
        self.s = s
        self.t = t
        G = EdgeWeightedDigraph(2 + 2 * n)
        for i in range(n):
            G.add_edge(DirectedEdge(i, i + n, duration[i]))
            G.add_edge(DirectedEdge(s, i, 0.))
            G.add_edge(DirectedEdge(i + n, t, 0.))
            for p in precedence[i]:
                G.add_edge(DirectedEdge(i + n, p, 0.))
        self.lp = AcyclicLP(G, s)

    def start_time(self):
        return {i: self.lp.dist_to[i] for i in range(self.n)}

    def finish_time(self):
        return self.lp.dist_to[self.t]
