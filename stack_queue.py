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


class PriorityQueueMax:
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


class PriorityQueueMin:
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


class IndexPriorityQueueMin:
    def __init__(self, max_n):
        # binary heap using 1-based indexing
        # pq[i] is the index of the key in heap position i
        self.pq = [-1] * (max_n + 1)
        # qp[] is the inverse function of pq[],
        # qp[pq[i]] = pq[qp[i]] = i,
        # i.e., the heap position of the key at index k is qp[k]
        self.qp = [-1] * max_n
        self.keys = [None] * max_n  # keys[pq[i]] is the key in heap position i
        self.N = 0

    def insert(self, i, key):
        '''
        associate key with index i
        '''
        if self.contains(i):
            raise ValueError(f"key index {i} is already in the priority queue")
        self.N += 1
        self.qp[i] = self.N
        self.pq[self.N] = i
        self.keys[i] = key
        self._swim(self.N)

    def del_min(self, return_key=False):
        '''
        remove a minimum key and return its associated index
        '''
        if self.N == 0:
            raise RuntimeError("The priority queue is empty")
        min_key_index = self.pq[1]
        self._exch(1, self.N)
        self.N -= 1
        self._sink(1)
        self.qp[min_key_index] = -1
        if return_key:
            min_key = self.keys[min_key_index]
            self.keys[min_key_index] = None
            return min_key_index, min_key
        else:
            self.keys[min_key_index] = None
            return min_key_index

    def change_key(self, i, key):
        if not self.contains(i):
            raise ValueError(f"key index {i} is not in the priority queue")
        self.keys[i] = key
        heap_index = self.qp[i]
        self._swim(heap_index)
        self._sink(heap_index)

    def increase_key(self, i, key):
        if not self.contains(i):
            raise ValueError(f"key index {i} is not in the priority queue")
        if key == self.keys[i]:
            raise ValueError("Calling increase_key() with a key equal to the key in the priority queue")
        elif key < self.keys[i]:
            raise ValueError("Calling increase_key() with a key strictly less than the key in the priority queue")
        self.keys[i] = key
        self._sink(self.qp[i])

    def decrease_key(self, i, key):
        if not self.contains(i):
            raise ValueError(f"key index {i} is not in the priority queue")
        if key == self.keys[i]:
            raise ValueError("Calling decrease_key() with a key equal to the key in the priority queue")
        elif key > self.keys[i]:
            raise ValueError("Calling decrease_key() with a key strictly greater than the key in the priority queue")
        self.keys[i] = key
        self._swim(self.qp[i])

    def min_key(self):
        '''
        return the minimum key
        '''
        if self.N == 0:
            raise RuntimeError("The priority queue is empty")
        return self.keys[self.pq[1]]

    def min_index(self):
        '''
        return the key index associated with the minimum key
        '''
        if self.N == 0:
            raise RuntimeError("The priority queue is empty")
        return self.pq[1]

    def contains(self, i):
        '''
        Is key index i associated with some item on this PQ?
        '''
        return self.qp[i] != -1

    def size(self):
        return self.N

    def delete(self, i):
        '''
        remove the key associated with index i
        '''
        if not self.contains(i):
            raise ValueError(f"key index {i} is not in the priority queue")
        heap_index = self.qp[i]
        self._exch(heap_index, self.N)
        self.N -= 1
        self._swim(heap_index)  # not needed?
        self._sink(heap_index)
        self.keys[i] = None
        self.qp[i] = -1

    def is_empty(self):
        return self.N == 0

    def _swim(self, k):
        while (k > 1) and self._greater(k // 2, k):
            self._exch(k // 2, k)
            k = k // 2

    def _sink(self, k):
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
        return self.keys[self.pq[i]] > self.keys[self.pq[j]]

    def _exch(self, i, j):
        self.pq[i], self.pq[j] = self.pq[j], self.pq[i]
        # to maintain the inverse relation
        self.qp[self.pq[i]] = i
        self.qp[self.pq[j]] = j
