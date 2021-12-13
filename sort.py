import random


def selection_sort(a):
    N = len(a)
    for i in range(0, N - 1):
        idx_min = i
        for j in range(i + 1, N):
            if a[j] < a[idx_min]:
                idx_min = j
        a[i], a[idx_min] = a[idx_min], a[i]


def insertion_sort(a):
    N = len(a)
    for i in range(1, N):
        for j in range(i, 0, -1):
            if a[j] < a[j - 1]:
                a[j], a[j - 1] = a[j - 1], a[j]
                j -= 1
            else:
                break


def insertion_sort_bounded(a, low, high):
    for i in range(low + 1, high + 1):
        for j in range(i, low, -1):
            if a[j] < a[j - 1]:
                a[j], a[j - 1] = a[j - 1], a[j]
                j -= 1
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

    def sort(self, a, aux, low, high):
        if high <= low:
            return
        mid = low + (high - low) // 2
        self.sort(a, aux, low, mid)
        self.sort(a, aux, mid + 1, high)
        self.merge(a, aux, low, mid, high)

    def merge(self, a, aux, low, mid, high):
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

    def merge_sort(self, a):
        aux = [0] * len(a)
        self.sort(a, aux, 0, len(a) - 1)


class MergeSortV2:
    def __init__(self, cutoff=None):
        self.cutoff = cutoff

    def merge(self, a, aux, low, mid, high):
        # ----- improvement1 -----
        if aux[mid] <= aux[mid + 1]:
            for m in range(low, high+1):
                a[m] = aux[m]
            return
        # ----------
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

    def sort(self, a, aux, low, high):
        if high <= low:
            return
        # ----- improvement -----
        if self.cutoff is not None:
            if high - low + 1 <= self.cutoff:
                insertion_sort_bounded(aux, low, high)
                return
        # ----------
        mid = low + (high - low) // 2
        self.sort(aux, a, low, mid)
        self.sort(aux, a, mid + 1, high)
        self.merge(aux, a, low, mid, high)

    def merge_sort(self, a):
        aux = a.copy()
        self.sort(aux, a, 0, len(a) - 1)


class QuickSort:
    def __init__(self, cutoff=None):
        self.cutoff = cutoff
    
    def sort(self, a, low, high):
        if low >= high:
            return
        # ----- improvement -----
        if self.cutoff is not None:
            if high - low + 1 <= self.cutoff:
                insertion_sort_bounded(a, low, high)
                return
        # ----------
        j = self.partition(a, low, high)
        self.sort(a, low, j - 1)
        self.sort(a, j + 1, high)

    def quick_sort(self, a):
        random.shuffle(a)
        self.sort(a, 0, len(a) - 1)

    def partition(self, a, low, high):
        # ----- improvement -----
        m = median_of_three(a, low, low + (high - low) // 2, high)
        a[low], a[m] = a[m], a[low]
        # ----------
        i = low
        j = high + 1
        while True:
            while True:
                i += 1
                if (not a[i] < a[low]) or i == high:
                    break
            while True:
                j -= 1
                if not a[j] > a[low]:
                    break
            if i >= j:
                break
            a[i], a[j] = a[j], a[i]
        a[j], a[low] = a[low], a[j]
        return j

    def selection(self, a, k):
        low = 0
        high = len(a) - 1
        while low < high:
            j = self.partition(a, low, high)
            if j < k:
                low = j + 1
            elif j > k:
                high = j - 1
            else:
                return a[k]
        return a[k]


class ThreeWayQuickSort:
    def __init__(self, cutoff=None):
        self.cutoff = cutoff

    def quick_sort(self, a):
        random.shuffle(a)
        self.sort(a, 0, len(a) - 1)

    def sort(self, a, low, high):
        if low >= high:
            return
        if self.cutoff is not None:
            if high - low + 1 <= self.cutoff:
                insertion_sort_bounded(a, low, high)
                return
        lt, gt = self.partition(a, low, high)
        self.sort(a, low, lt - 1)
        self.sort(a, gt + 1, high)

    def partition(self, a, low, high):
        # ----- improvement -----
        m = median_of_three(a, low, low + (high - low) // 2, high)
        a[low], a[m] = a[m], a[low]
        # ----------
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


class Heap:
    def __init__(self):
        pass

    def sort(self, a):
        N = len(a)
        # firstly construct the heap
        for k in range(N//2, 0, -1):
            self.sink(a, k, N)
        # sort
        for k in range(N, 0, -1):
            self.exchange(a, 1, N)
            N -= 1
            self.sink(a, 1, N)

    def sink(self, a, k, N):
        # exchange key in parent with key in the larger children
        # used after exchange
        # sink preserve the binary heap in the subtree
        # complexity 2logN compares
        # sink on a node will give a binary heap, given that the node's subtree are both binary heaps
        while 2*k <= N:
            j = k * 2
            if j < N and self.less(a, j, j+1):
                j += 1
            if self.less(a, k, j):
                self.exchange(a, k, j)
            else:
                break
            k = j

    def exchange(self, a, i, j):
        # convert from 1-based index to 0-based index
        a[i-1], a[j-1] = a[j-1], a[i-1]

    def less(self, a, i, j):
        # convert from 1-based index to 0-based index
        return a[i-1] < a[j-1]



