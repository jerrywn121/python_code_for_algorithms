from stack_queue import Queue


class Node:
    def __init__(self, key, value, left=None, right=None, color=None):
        self.key = key
        self.value = value
        self.left = left
        self.right = right
        self.color = color
        self.count = 1


class BinarySearchTree:
    '''
    better than binary search of ordered array in terms of the complexity of the "put" method.
    For binary search we need to maintain an ordered array and every time
    we insert an item we need to shift all larger items right, resulting in
    a O(N) complexity.
    But the performance of the binary search tree requires that the keys
    are inserted in random order, which may not be satisfied as the client
    may not provide randomized keys.
    '''
    def __init__(self):
        self.root = None

    def get(self, key):
        x = self.root
        while x is not None:
            if x.key < key:
                x = x.right
            elif x.key > key:
                x = x.left
            else:
                return x.value
        return None

    def put(self, key, value):
        self.root = self._put_helper(self.root, key, value)

    def _put_helper(self, x, key, value):
        '''
        put the key and value within the subtree rooted at x
        and return the modified subtree
        '''
        if x is None:
            return Node(key, value)
        if x.key < key:
            x.right = self._put_helper(x.right, key, value)
        elif x.key > key:
            x.left = self._put_helper(x.left, key, value)
        else:
            x.value = value
        x.count = 1 + self._size(x.left) + self._size(x.right)
        return x

    def delete(self, key):
        '''
        Hibbard deletion
        '''
        if self.root is not None:
            self.root = self._delete_helper(self.root, key)

    def _delete_helper(self, x, key):
        '''
        delete the key in the tree whose root is x
        and return the modified tree
        '''
        if x is None:
            return None
        if key < x.key:
            x.left = self._delete_helper(x.left, key)
        elif key > x.key:
            x.right = self._delete_helper(x.right, key)
        else:  # key == x.key
            if x.right is None:
                return x.left
            if x.left is None:
                return x.right
            t = x
            x = self._min_helper(t.right)
            # note that we must modify x.right before x.left
            # otherwise when we call x.left = t.left
            # the t.right will also be altered
            x.right = self._delete_min_helper(t.right)  # delete_min_helper(t.right) also alters t in place
            x.left = t.left

        x.count = 1 + self._size(x.left) + self._size(x.right)
        return x

    def delete_min(self):
        if self.root is not None:
            self.root = self._delete_min_helper(self.root)

    def _delete_min_helper(self, x):
        '''
        delete the min in the tree whose root is x in place
        and return the modified tree
        '''
        if x.left is None:
            return x.right
        x.left = self._delete_min_helper(x.left)
        x.count = 1 + self._size(x.left) + self._size(x.right)
        return x

    def size(self):
        return self._size(self.root)

    def _size(self, x):
        if x is None:
            return 0
        return x.count

    def max(self):
        x = self.root
        if x is None:
            return None
        while x.right is not None:
            x = x.right
        return x.key

    def min(self):
        x = self.root
        if x is None:
            return None
        while x.left is not None:
            x = x.left
        return x.key

    def _min_helper(self, x):
        if x is None:
            return None
        while x.left is not None:
            x = x.left
        return x

    def floor(self, key):
        x = self._floor_helper(self.root, key)
        if x is None:
            return None
        return x.key

    def _floor_helper(self, x, key):
        '''
        find the largest key in the subtree rooted at x that is smaller than key
        return the node containing this key
        '''
        if x is None:
            return None

        if key == x.key:
            return x

        if key < x.key:
            # the result must be the floor of the left subtree
            return self._floor_helper(x.left, key)

        t = self._floor_helper(x.right, key)
        if t is not None:
            return t
        else:
            return x

    def select(self, k):
        '''
        return node
        '''
        assert k < self.size()
        return self._select_helper(self.root, k).key

    def _select_helper(self, x, k):
        '''
        return the node containing the key whose rank is k in the subtree rooted at x
        '''
        if x is None:
            return None

        t = self._size(x.left)
        if t > k:
            return self._select_helper(x.left, k)
        elif t < k:
            return self._select_helper(x.right, k - t - 1)
        else:
            return x

    def rank(self, key):
        return self._rank_helper(key, self.root)

    def _rank_helper(self, key, x):
        '''
        return the rank (how many keys < key) of the key
        in the subtree rooted at x
        '''
        if x is None:
            return 0
        if key > x.key:
            return 1 + self._size(x.left) + self._rank_helper(key, x.right)
        if key < x.key:
            return self._rank_helper(key, x.left)
        return self._size(x.left)  # key == x.key

    def inorder_traversal(self):
        x = []
        self._inorder(self.root, x)
        return x

    def _inorder(self, x, a):
        '''
        add the keys in the subtree rooted at x in ascending order to a
        '''
        if x is None:
            return
        self._inorder(x.left, a)
        a.append(x.key)
        self._inorder(x.right, a)

    def level_order_traversal(self):
        queue = Queue()
        queue.enqueue(self.root)
        a = []
        while not queue.is_empty():
            x = queue.dequeue()
            if x is not None:
                a.append(x.key)
                queue.enqueue(x.left)
                queue.enqueue(x.right)
        return a


class RedBlackBST(BinarySearchTree):
    def __init__(self):
        super().__init__()
        self.root = None
        self._RED = True
        self._BLACK = False

    def _is_red(self, h):
        if h is None:
            return False
        return h.color == self._RED

    def _rotate_left(self, h):
        x = h.right
        h.right = x.left
        x.left = h
        x.color = h.color
        h.color = self._RED
        x.count = h.count
        h.count = 1 + self._size(h.left) + self._size(h.right)
        return x

    def _rotate_right(self, h):
        x = h.left
        h.left = x.right
        x.right = h
        x.color = h.color
        h.color = self._RED
        x.count = h.count
        h.count = 1 + self._size(h.left) + self._size(h.right)
        return x

    def _flip_colors(self, h):
        h.color = self._RED
        h.left.color = self._BLACK
        h.right.color = self._BLACK

    def put(self, key, value):
        self.root = self._put_helper(self.root, key, value)
        self.root.color = self._BLACK

    def _put_helper(self, h, key, value):
        if h is None:
            return Node(key, value, color=self._RED)
        if key < h.key:
            h.left = self._put_helper(h.left, key, value)
        elif key > h.key:
            h.right = self._put_helper(h.right, key, value)
        else:
            h.value = value

        # consider inserting into a two-node and a three-node
        # we need only the first if condition for inserting into a two-node (h.left and h.right are black originally)
        # but we need all three if conditions for inserting into a three-node (h.left is red and h.right is black originally)
        if (not self._is_red(h.left)) and self._is_red(h.right):
            h = self._rotate_left(h)
        if self._is_red(h.left) and self._is_red(h.left.left):
            h = self._rotate_right(h)
        if self._is_red(h.left) and self._is_red(h.right):
            self._flip_colors(h)
        h.count = 1 + self._size(h.left) + self._size(h.right)
        return h

    def get(self, key):
        x = self.root
        while x is not None:
            if x.key < key:
                x = x.right
            elif x.key > key:
                x = x.left
            else:
                return x.value
        return None

    def _size(self, x):
        if x is None:
            return 0
        return x.count
