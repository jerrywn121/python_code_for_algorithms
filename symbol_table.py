class SymbolTable:
    def __init__(self):
        self.N = 0
        self.keys = []
        self.values = []
    
#     def put(self):
#         # overwrite old value
#         # remove key-value pair if value is None
        
#     def get(self):
#         # null if key is absent
        
    def delete(self):
        self.put(key, None)

    def contains(self, key):
        return self.get(key) is not None

    def is_empty(self):
        return self.N == 0

    def size(self):
        return self.N

    def keys(self):
        return self.keys


class BinarySearchSymbolTable(SymbolTable):
    '''
    maintain an ordered keys and values and use binary search
    '''
    def __init__(self):
        super().__init__()

    def put(self, key, value):
        # overwrite old value
        # remove key-value pair if value is None
        ### shift
        k = self.rank(key)
        self.keys.insert(k, key)
        self.values.insert(k, value)

    def get(self, key):
        # null if key is absent
        if self.is_empty:
            return None
        i = self.rank(key)
        if i < self.N and self.keys[i] == key:
            return self.values[i]
        return None
    
    def rank(self, key):
        low = 0
        high = len(self.keys) - 1
        while low <= high:
            mid = low + (high - low) // 2
            if self.keys[mid] < key:
                low = mid + 1
            elif self.keys[mid] < key:
                high = mid - 1
            else:
                return mid
        return low  # the returned low is guranteed to be larger than 0


class Node:
    def __init__(self, key, value, left=None, right=None):
        self.key = key
        self.value = value
        self.left = left
        self.right = right
        self.count = 1


class BinarySearchTree:
    '''
    better than binary search in terms of the complexity of the "put" method.
    For binary search we need to maintain an ordered array and every time
    we insert an item we need to shift all larger items right, resulting in
    a O(N) complexity.
    But the performance of the binary search tree requires that the keys
    are inserted in random order, which may not be satisfied as the client
    may not provide randomized keys.
    '''
    def __init__(self):
        self.root = None

#     def get(self, key):
#         return self.get_helper(self.root, key)

#     def get_helper(self, root, key):
#         if root is None:
#             return None
#         if key < root.key:
#             return self.get_helper(root.left, key)
#         elif key > root.key:
#             return self.get_helper(root.right, key)
#         else:
#             return root.value

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
        # the reason why we don't use the same steps in
        # get is that we
        # need to modify every node to link to a new subtree
        # random insertion is needed to ensure performance
        self.root = self.put_helper(self.root, key, value)

    def put_helper(self, x, key, value):
        # put the key and value within the tree whose root is x
        # and return the modified tree
        if x is None:
            return Node(key, value)
        if x.key < key:
            x.right = self.put_helper(x.right, key, value)
        elif x.key > key:
            x.left = self.put_helper(x.left, key, value)
        else:
            x.value = value
        x.count = 1 + self.size(x.left) + self.size(x.right)
        return x

    def delete(self, key):
        '''
        Hibbard deletion
        '''
        if self.root is not None:
            self.root = self.delete_helper(self.root, key)

    def delete_helper(self, x, key):
        '''
        delete the key in the tree whose root is x
        and return the modified tree
        '''
        if x is None:
            return None
        if key < x.key:
            x.left = self.delete_helper(x.left, key)
        elif key > x.key:
            x.right = self.delete_helper(x.right, key)
        else:  # key == x.key
            if x.right is None:
                return x.left
            if x.left is None:
                return x.right
            t = x
            x = self.min_helper(t.right)
            # note that we must modify x.right before x.left
            # otherwise when we call x.left = t.left
            # the t.right will also be altered
            x.right = self.delete_min_helper(t.right)  # delete_min_helper(t.right) also alters t in place
            x.left = t.left

        x.count = 1 + self.size(x.left) + self.size(x.right)
        return x

    def delete_min(self):
        if self.root is not None:
            self.root = self.delete_min_helper(self.root)

    def delete_min_helper(self, x):
        '''
        delete the min in the tree whose root is x in place
        and return the modified tree
        '''
        if x.left is None:
            return x.right
        x.left = self.delete_min_helper(x.left)
        x.count = 1 + self.size(x.left) + self.size(x.right)
        return x

    def size(self, x):
        if x is None:
            return 0
        return x.count

    def max(self):
        x = self.root
        if x is None:
            return None
        while x.right is not None:
            x = x.right
        return x

    def min(self):
        x = self.root
        if x is None:
            return None
        while x.left is not None:
            x = x.left
        return x

    def min_helper(self, x):
        if x is None:
            return None
        while x.left is not None:
            x = x.left
        return x

    def floor(self, key):
        x = self.floor_helper(self.root, key)
        if x is None:
            return None
        return x.key

    def floor_helper(self, x, key):
        '''
        returns the largest key smaller than "key" in the tree whose root is x
        '''
        if root is None:
            return None

        if key == x.key:
            return x

        if key < x.key:
            # the result must be the floor of the left subtree
            return self.floor_helper(x.left, key)

        t = self.floor_helper(x.right, key)
        if t is not None:
            return t
        else:
            return x

    def rank(self, key):
        return self.rank_helper(key, self.root)

    def rank_helper(self, key, x):
        '''
        returns the rank (how many keys < key) of the key
        in the tree whose node is x
        '''
        if x is None:
            return 0
        if key > x.key:
            return 1 + self.size(x.left) + self.rank_helper(key, x.right)
        if key < x.key:
            return self.rank_helper(key, x.left)
        return self.size(x.left)  # key == x.key

    def inorder_traversal(self):
        x = []
        self.inorder(self.root, x)
        return x

    def inorder(self, x, a):
        '''
        add the keys in the tree whose root is x in ascending order to a
        '''
        if x is None:
            return
        self.inorder(x.left, a)
        a.append(x.key)
        self.inorder(x.right, a)


class RedBlackBST:
    def __init__(self):
        self.root = None
        self._RED = True
        self._BLACK = False

    def is_red(self, h):
        if h is None:
            return False
        return h.color == self._RED

    def rotate_left(self, h):
        x = h.right
        h.right = x.left
        x.left = h
        x.color = h.color
        h.color = self._RED
        x.count = h.count
        h.count = 1 + self.size(h.left) + self.size(h.right)
        return x

    def rotate_right(self, h):
        x = h.left
        h.left = x.right
        x.right = h
        x.color = h.color
        h.color = self._RED
        x.count = h.count
        h.count = 1 + self.size(h.left) + self.size(h.right)
        return x
    
    def flip_colors(self, h):
        h.color = self._RED
        h.left.color = self._BLACK
        h.right.color = self._BLACK
    
    def put(self, key, value):
        self.root = self.put_helper(self.root, key, value)
        self.root.color = self._BLACK

    def put_helper(self, h, key, value):
        if h is None:
            return Node(key, value, color=self._RED)
        if key < h.key:
            h.left = self.put_helper(h.left, key, value)
        elif key > h.key:
            h.right = self.put_helper(h.right, key, value)
        else:
            h.value = value

        # consider inserting into a two-node and a three-node
        # we need only the first if condition for inserting into a two-node (h.left and h.right are black originally)
        # but we need all three if conditions for inserting into a three-node (h.left is red and h.right is black originally)
        if (not self.is_red(h.left)) and self.is_red(h.right):
            h = self.rotate_left(h)
        if self.is_red(h.left) and self.is_red(h.left.left):
            h = self.rotate_right(h)
        if self.is_red(h.left) and self.is_red(h.right):
            self.flip_colors(h)
        h.count = 1 + self.size(h.left) + self.size(h.right)
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

    def size(self, x):
        if x is None:
            return 0
        return x.count


def printBinaryTree(root, space=1, height=10):
    # Base case
    if root is None:
        return
 
    # increase distance between levels
    space += height

    # print right child first
    printBinaryTree(root.right, space, height)
    print()

    # print the current node after padding with spaces
    for i in range(height, space):
        print(' ', end='')
 
    print(str(root.key) + ":" + str(root.value) + ":" + str(root.count), end='')
 
    # print left child
    print()
    printBinaryTree(root.left, space, height)
