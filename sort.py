import random


def selection_sort(a):
    '''
    (NOT STABLE)
    At each iteration i, find the index (idx_min) of smallest remaining entries to its right,
    swap a[i] and a[idx_min].
    '''
    N = len(a)
    for i in range(N - 1):
        idx_min = i
        for j in range(i + 1, N):
            if a[j] < a[idx_min]:
                idx_min = j
        a[i], a[idx_min] = a[idx_min], a[i]


def insertion_sort(a):
    '''
    (STABLE)
    At each iteration i, indices from 0 to i-1 have been sorted.
    Swap a[i] with every larger entry to its left,
    such that 0 to i is sorted.
    '''
    N = len(a)
    for i in range(1, N):
        for j in range(i, 0, -1):
            if a[j] < a[j - 1]:
                a[j], a[j - 1] = a[j - 1], a[j]
            else:
                break


def insertion_sort_bounded(a, low, high):
    for i in range(low + 1, high + 1):
        for j in range(i, low, -1):
            if a[j] < a[j - 1]:
                a[j], a[j - 1] = a[j - 1], a[j]
            else:
                break


def median_of_three(a, low, mid, high):
    if a[low] < a[mid]:
        if a[mid] < a[high]:
            return mid
        elif a[low] < a[high]:
            return high
        else:
            return low
    # a[low] >= a[mid]
    else:
        if a[mid] > a[high]:
            return mid
        elif a[low] > a[high]:
            return high
        else:
            return low


class MergeSort:
    def __init__(self):
        pass

    def _sort_helper(self, a, aux, low, high):
        if high <= low:
            return
        mid = low + (high - low) // 2
        self._sort_helper(a, aux, low, mid)
        self._sort_helper(a, aux, mid + 1, high)
        self._merge(a, aux, low, mid, high)

    def _merge(self, a, aux, low, mid, high):
        '''
        merge from aux to a
        '''
        for m in range(low, high+1):
            aux[m] = a[m]
        i = low
        j = mid + 1
        for k in range(low, high+1):
            if i > mid:
                a[k] = aux[j]
                j += 1
            elif j > high:
                a[k] = aux[i]
                i += 1
            elif aux[i] > aux[j]:
                a[k] = aux[j]
                j += 1
            else:
                a[k] = aux[i]
                i += 1

    def sort(self, a):
        aux = [0] * len(a)
        self._sort_helper(a, aux, 0, len(a) - 1)


class MergeSortV2:
    def __init__(self, cutoff=0):
        self.cutoff = cutoff

    def _merge(self, a, aux, low, mid, high):
        '''
        merge from aux to a
        '''
        if aux[mid] <= aux[mid + 1]:
            for m in range(low, high+1):
                a[m] = aux[m]
            return
        i = low
        j = mid + 1
        for k in range(low, high+1):
            if i > mid:
                a[k] = aux[j]
                j += 1
            elif j > high:
                a[k] = aux[i]
                i += 1
            elif aux[i] > aux[j]:
                a[k] = aux[j]
                j += 1
            else:
                a[k] = aux[i]
                i += 1

    def _sort_helper(self, a, aux, low, high):
        '''
        sort aux given the auxiliary array a
        '''
        if high <= low:
            return
        if high - low + 1 <= self.cutoff:
            insertion_sort_bounded(aux, low, high)
            return
        mid = low + (high - low) // 2
        # the following two lines treat aux as auxiliary array
        # (merge from aux to a)
        self._sort_helper(aux, a, low, mid)
        self._sort_helper(aux, a, mid + 1, high)
        # this merges from a to aux (a is the auxiliary array)
        self._merge(aux, a, low, mid, high)

    def sort(self, a):
        aux = a.copy()
        self._sort_helper(aux, a, 0, len(a) - 1)


class QuickSort:
    def __init__(self, cutoff=0):
        self.cutoff = cutoff

    def _sort_helper(self, a, low, high):
        if high <= low:
            return
        if high - low + 1 <= self.cutoff:
            insertion_sort_bounded(a, low, high)
            return
        j = self._partition(a, low, high)
        self._sort_helper(a, low, j - 1)
        self._sort_helper(a, j + 1, high)

    def sort(self, a):
        random.shuffle(a)
        self._sort_helper(a, 0, len(a) - 1)

    def _partition(self, a, low, high):
        m = median_of_three(a, low, low + (high - low) // 2, high)
        a[low], a[m] = a[m], a[low]
        i = low
        j = high + 1
        v = a[low]
        while True:
            while True:
                i += 1
                if a[i] >= v or i == high:
                    break
            while True:
                j -= 1
                if a[j] <= v:
                    break
            if i >= j:
                break
            a[i], a[j] = a[j], a[i]
        a[j], a[low] = a[low], a[j]
        return j

    def select(self, a, k):
        random.shuffle(a)
        low = 0
        high = len(a) - 1
        while low < high:
            j = self._partition(a, low, high)
            if j < k:
                low = j + 1
            elif j > k:
                high = j - 1
            else:
                return a[k]
        return a[k]


class ThreeWayQuickSort:
    def __init__(self, cutoff=0):
        self.cutoff = cutoff

    def sort(self, a):
        random.shuffle(a)
        self._sort_helper(a, 0, len(a) - 1)

    def _sort_helper(self, a, low, high):
        if low >= high:
            return
        if high - low + 1 <= self.cutoff:
            insertion_sort_bounded(a, low, high)
            return
        lt, gt = self._partition(a, low, high)
        self._sort_helper(a, low, lt - 1)
        self._sort_helper(a, gt + 1, high)

    def _partition(self, a, low, high):
        m = median_of_three(a, low, low + (high - low) // 2, high)
        a[low], a[m] = a[m], a[low]
        lt = low
        i = low + 1
        gt = high
        v = a[low]
        while i <= gt:
            if a[i] < v:
                a[i], a[lt] = a[lt], a[i]
                i += 1
                lt += 1
            elif a[i] > v:
                a[i], a[gt] = a[gt], a[i]
                gt -= 1
            else:
                i += 1
        return lt, gt


class HeapSort:
    def __init__(self):
        pass

    def sort(self, a):
        N = len(a)
        # construct the heap
        for k in range(N//2, 0, -1):
            self._sink(a, k, N)
        # sort
        while N > 1:
            self._exch(a, 1, N)
            N -= 1
            self._sink(a, 1, N)

    def _sink(self, a, k, N):
        '''
        Exchange key in parent with key in the larger child,
        when parent's key becomes smaller than one (or both) of its children's.
        Repeat until heap order restored
        '''
        while 2*k <= N:
            j = k * 2
            if j < N and self._less(a, j, j+1):
                j += 1
            if self._less(a, k, j):
                self._exch(a, k, j)
            else:
                break
            k = j

    def _less(self, a, i, j):
        # convert from 1-based index to 0-based index
        return a[i-1] < a[j-1]

    def _exch(self, a, i, j):
        # convert from 1-based index to 0-based index
        a[i-1], a[j-1] = a[j-1], a[i-1]
