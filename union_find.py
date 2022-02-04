class UnionFind:
    def __init__(self, n):
        self.id = list(range(n))
        self.sz = [1] * n
        self.count = n

    def find(self, i):
        return self.root(i)

    def root(self, i):
        while self.id[i] != i:
            self.id[i] = self.id[self.id[i]]
            i = self.id[i]
        return i

    def union(self, p, q):
        i = self.root(p)
        j = self.root(q)
        if i == j:
            return
        if self.sz[i] < self.sz[j]:
            self.id[i] = j
            self.sz[j] += self.sz[i]
        else:
            self.id[j] = i
            self.sz[i] += self.sz[j]
        self.count -= 1

    def connected(self, p, q):
        return self.root(p) == self.root(q)

    def count(self):
        return self.count
