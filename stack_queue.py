class Node:
    def __init__(self, item, next=None):
        self.item = item
        self.next = next


class Stack:
    def __init__(self):
        self.first = None
        self.N = 0

    def push(self, item):
        self.first = Node(item, self.first)
        self.N += 1

    def pop(self):
        item = self.first.item
        self.first = self.first.next
        self.N -= 1
        return item

    def is_empty(self):
        return self.first is None

    def size(self):
        return self.N

    def tolist(self):
        values = []
        current = self.first
        while current is not None:
            values.append(current.item)
            current = current.next
        return values

    def __str__(self):
        return '->'.join([str(i) for i in self.tolist()])


class Queue:
    def __init__(self):
        self.first = None
        self.last = None
        self.N = 0

    def enqueue(self, item):
        if self.is_empty():
            self.first = Node(item)
            self.last = self.first
        else:
            oldlast = self.last
            self.last = Node(item)
            oldlast.next = self.last
        self.N += 1

    def dequeue(self):
        item = self.first.item
        self.first = self.first.next
        if self.is_empty():
            self.last = None
        self.N -= 1
        return item

    def is_empty(self):
        return self.first is None

    def size(self):
        return self.N

    def tolist(self):
        values = []
        current = self.first
        while current is not None:
            values.append(current.item)
            current = current.next
        return values

    def __str__(self):
        return '->'.join([str(i) for i in self.tolist()])


class PriorityQueueBinaryHeapMax:
    '''
    binary heap implementation of max-oriented priority queue
    '''
    def __init__(self):
        self.pq = [None]  # the index start at 1
        self.N = 0

    def insert(self, x):
        self.pq.append(x)
        self.N += 1
        self._swim(self.N)

    def del_max(self):
        self._exch(1, -1)
        max_ = self.pq.pop()
        self.N -= 1
        self._sink(1)
        return max_

    def is_empty(self):
        return self.N == 0

    def max(self):
        return self.pq[1]

    def size(self):
        return self.N

    def _swim(self, k):
        '''
        Exchange key in child with the key in parent,
        when child's key becomes larger than its parent's key.
        Repeat until heap order restored
        '''
        while (k > 1) and self._less(k // 2, k):
            self._exch(k // 2, k)
            k = k // 2

    def _sink(self, k):
        '''
        Exchange key in parent with key in the larger child,
        when parent's key becomes smaller than one (or both) of its children's.
        Repeat until heap order restored
        '''
        while 2*k <= self.N:
            j = k * 2
            if j < self.N and self._less(j, j+1):
                j += 1
            if self._less(k, j):
                self._exch(k, j)
            else:
                break
            k = j

    def _less(self, i, j):
        return self.pq[i] < self.pq[j]

    def _exch(self, i, j):
        self.pq[i], self.pq[j] = self.pq[j], self.pq[i]


class PriorityQueueBinaryHeapMin:
    '''
    binary heap implementation of min-oriented priority queue
    '''
    def __init__(self):
        self.pq = [None]  # the index start at 1
        self.N = 0

    def insert(self, x):
        self.pq.append(x)
        self.N += 1
        self._swim(self.N)

    def del_min(self):
        self._exch(1, -1)
        min_ = self.pq.pop()
        self.N -= 1
        self._sink(1)
        return min_

    def is_empty(self):
        return self.N == 0

    def min(self):
        return self.pq[1]

    def size(self):
        return self.N

    def _swim(self, k):
        '''
        Exchange key in child with the key in parent,
        when child's key becomes smaller than its parent's key.
        Repeat until heap order restored
        '''
        while (k > 1) and self._greater(k // 2, k):
            self._exch(k // 2, k)
            k = k // 2

    def _sink(self, k):
        '''
        Exchange key in parent with key in the larger child,
        when parent's key becomes greater than one (or both) of its children's.
        Repeat until heap order restored
        '''
        while 2*k <= self.N:
            j = k * 2
            if j < self.N and self._greater(j, j+1):
                j += 1
            if self._greater(k, j):
                self._exch(k, j)
            else:
                break
            k = j

    def _greater(self, i, j):
        return self.pq[i] > self.pq[j]

    def _exch(self, i, j):
        self.pq[i], self.pq[j] = self.pq[j], self.pq[i]
