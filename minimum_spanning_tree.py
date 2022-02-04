from stack_queue import Queue, PriorityQueueMin, IndexPriorityQueueMin
from union_find import UnionFind


class KruskalMST:
    def __init__(self, G):
        self.mst = Queue()
        pq = PriorityQueueMin()
        uf = UnionFind(G.V)
        for e in G.edges():
            pq.insert(e)
        while not pq.is_empty() and self.mst.N < G.V - 1:
            e = pq.del_min()
            v = e.either()
            w = e.other(v)
            if not uf.connected(v, w):
                uf.union(v, w)
                self.mst.enqueue(e)

    def edges(self):
        return self.mst

    def weight(self):
        return sum([x.weight for x in self.mst.tolist()])


class PrimLazyMst:
    '''
    lazy version of Prim's MST algorithm
    '''
    def __init__(self, G):
        self.mst = Queue()  # mst edges
        pq = PriorityQueueMin()  # crossing edges
        self.marked = [False] * G.V  # mst vertices
        self._visit(G, 0, pq)
        while not pq.is_empty() and self.mst.N < G.V - 1:
            e = pq.del_min()
            v = e.either()
            w = e.other(v)
            if self.marked[v]:
                if self.marked[w]:
                    continue
                else:
                    u = w
            else:
                u = v
            self.mst.enqueue(e)
            self._visit(G, u, pq)

    def _visit(self, G, v, pq):
        '''
        mark v and add to pq any non-tree edge incident onto v
        '''
        self.marked[v] = True
        for e in G.adj[v]:
            if not self.marked[e.other(v)]:
                pq.insert(e)

    def edges(self):
        return self.mst

    def weight(self):
        return sum([x.weight for x in self.mst.tolist()])


class PrimEagerMst:
    '''
    eager version of Prim's MST algorithm
    '''
    def __init__(self, G):
        self.mst = Queue()  # mst edges
        pq = IndexPriorityQueueMin(G.V)  # eligible crossing edges
        marked = [False] * G.V  # mst vertices
        marked[0] = True
        for e in G.adj[0]:
            pq.insert(e.other(0), e)

        while not pq.is_empty() and self.mst.N < G.V - 1:
            min_vertex, min_edge = pq.del_min(return_key=True)
            self.mst.enqueue(min_edge)
            marked[min_vertex] = True
            for e in G.adj[min_vertex]:
                v = e.other(min_vertex)
                # only consider non-tree vertex
                if marked[v]:
                    continue
                if not pq.contains(v):
                    # not on the pq before but is now connected to the tree
                    # and becomes an eligible edge
                    pq.insert(v, e)
                elif e < pq.keys[v]:
                    # already on the pq and has a min weight to the tree
                    pq.decrease_key(v, e)

    def edges(self):
        return self.mst

    def weight(self):
        return sum([x.weight for x in self.mst.tolist()])
