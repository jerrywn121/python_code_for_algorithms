class Node:
    def __init__(self, item, next=None):
        self.item = item
        self.next = next


class LinkedList:
    def __init__(self):
        self.first = None

    def is_empty(self):
        return self.first is None
    
    def push(self, item):
        # add in the beginning
        self.first = Node(item, self.first)
    
    def append(self, item):
        # add in the end
        last = Node(item)
        if not self.first:
            self.first = last
            return
        current = self.first
        while current.next:
            current = current.next
        current.next = last

    def pop(self):
        item = self.first.item
        self.first = self.first.next
        return item


class LinkedListStack:
    def __init__(self):
        self.first = None
        self.N = 0

    def is_empty(self):
        return self.first is None

    def push(self, item):
        self.first = Node(item, self.first)
        self.N += 1

    def pop(self):
        item = self.first.item
        self.first = self.first.next
        self.N -= 1
        return item

    def tolist(self):
        values = []
        current = self.first
        while current != None:
            values.append(current.item)
            current = current.next
        return values       

    def __str__(self):
        values = self.tolist()
        return '->'.join([str(i) for i in values])


class LinkedListQueue:
    def __init__(self):
        self.first = None
        self.last = None

    def is_empty(self):
        return self.first is None

    def enqueue(self, item):
        if self.is_empty():
            self.first = Node(item)
            self.last = self.first
        else:
            oldlast = self.last
            self.last = Node(item)
            oldlast.next = self.last

    def dequeue(self):
        item = self.first.item
        self.first = self.first.next
        if self.is_empty():
            self.last = None
        return item

    def tolist(self):
        values = []
        current = self.first
        while current != None:
            values.append(current.item)
            current = current.next
        return values       

    def __str__(self):
        values = self.tolist()
        return '->'.join([str(i) for i in values])


class PriorityQueueBinaryHeapMax:
    '''
    binary heap implementation of max-oriented priority queue
    '''
    def __init__(self):
        self.N = 0
        self.pq = [None]  # the index start at 1

    def insert(self, x):
        self.pq.append(x)
        self.N += 1
        self.swim(self.N)
    
    def del_max(self):
        self.pq[1], self.pq[-1] = self.pq[-1], self.pq[1]
        max = self.pq.pop()
        self.N -= 1
        self.sink(1)
        return max

    def is_empty(self):
        return self.N == 0

    def max(self):
        return self.pq[1]

    def size(self):
        return self.N

    def swim(self, k):
        # exchange key in child with the key in parent
        # when child's key becomes larger than its parent's key
        # note that swim preserves the binary heap of the parent's another node
        # used after insertion, with complexity logN compares
        while (k > 1) and self.less(k // 2, k):
            self.pq[k//2], self.pq[k] = self.pq[k], self.pq[k//2]
            k = k // 2

    def sink(self, k):
        # exchange key in parent with key in the larger children
        # used after exchange
        # sink preserve the binary heap in the subtree
        # complexity 2logN compares
        while 2*k <= self.N:
            j = k * 2
            if j < self.N and self.less(j, j+1):
                j += 1
            if self.less(k, j):
                self.pq[j], self.pq[k] = self.pq[k], self.pq[j]
            else:
                break
            k = j

    def less(self, i, j):
        return self.pq[i] < self.pq[j]


class PriorityQueueBinaryHeapMin:
    '''
    binary heap implementation of max-oriented priority queue
    '''
    def __init__(self):
        self.N = 0
        self.pq = [None]  # the index start at 1

    def insert(self, x):
        self.pq.append(x)
        self.N += 1
        self.swim(self.N)

    def del_min(self):
        self.pq[1], self.pq[-1] = self.pq[-1], self.pq[1]
        min = self.pq.pop()
        self.N -= 1
        self.sink(1)
        return min

    def is_empty(self):
        return self.N == 0

    def min(self):
        return self.pq[1]

    def size(self):
        return self.N

    def swim(self, k):
        # exchange key in child with the key in parent
        # when child's key becomes larger than its parent's key
        # note that swim preserves the binary heap of the parent's another node
        # used after insertion, with complexity logN compares
        while (k > 1) and self.greater(k // 2, k):
            self.pq[k//2], self.pq[k] = self.pq[k], self.pq[k//2]
            k = k // 2

    def sink(self, k):
        # exchange key in parent with key in the larger children
        # used after exchange
        # sink preserve the binary heap in the subtree
        # complexity 2logN compares
        while 2*k <= self.N:
            j = k * 2
            if j < self.N and self.greater(j, j+1):
                j += 1
            if self.greater(k, j):
                self.pq[j], self.pq[k] = self.pq[k], self.pq[j]
            else:
                break
            k = j

    def greater(self, i, j):
        return self.pq[i] > self.pq[j]
