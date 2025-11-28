#基本操作
import sys
input = sys.stdin.readline
from collections import deque
import bisect
import heapq
import math
import copy
import math

#lazyseg
class lasyseg:
    '''
    input like st = LazySegmentTree(list_data, defualt, クエリに対する計算lambda x, y: x + y, updateの計算xor...)
    +, -, *, min, max以外(XORなど)は修正必要

    funcの場合、lambda x, y: x + y, lambda x, y : x ^ yで実装可能
    lazy_funcの場合、lambda x, y: x + y、、などしかし、XORは注釈に用意したのでそれを利用する
    if update -> xorなら内部関数を修正
    他の場合、実装したほうが
    
    Example:
        st = lasyseg(
        list_data = [1, 2, 3, 4, 5],
        default = 0,
        func = lambda x, y: x + y,
        lazy_func = lambda cur, val, size: cur + val * size
    )

    st.update(1, 2, 10)  # index [1, 4) func 10
    st.update(2, 2, 10)  # index [2, 5) func 10
    print(st.query(0, 5))  # 総合和
    print(st.query(1, 3))  # 2+10 + 3+10 + 4+10 = 39
    print(st.point_query(num)) # index numをプリント

    '''

    def __init__(self, list_data, default, func, lazy_func):
        self.list_data = list_data
        self.data = [[default, None] for _ in range(len(list_data) * 4)]
        self.default = default
        self.func = func
        self.lazy_func = lazy_func
        self.build(1, 0, len(list_data) - 1)

    #Top-Down
    def build(self, node, left, right):
        if left == right:
            self.data[node][0] = self.list_data[left]
        else:
            mid = (left + right) // 2
            self.build(node * 2, left, mid)
            self.build(node * 2 + 1, mid + 1, right)
            self.data[node][0] = self.func(self.data[node * 2][0], self.data[node * 2 + 1][0])

    #Lazy-segment
    #場合によって修正必要
    def propagate(self, node, left, right):
        if self.data[node][1] is None:
            return
    
        if self.data[node][1] is not None:

            check_num = right - left + 1
            self.data[node][0] += self.lazy_func(self.data[node][1], check_num)
            #if xor
            # if check_num % 2:
            #     self.data[node][0] ^= self.data[node][1]


            if left != right:
                for child in [node * 2, node * 2 + 1]:
                    if self.data[child][1] is None:
                        self.data[child][1] = self.data[node][1]
                    else:

                        #場合によって修正必要
                        self.data[child][1] += self.data[node][1]
                        #if xor
                        #self.data[child][1] ^= self.data[node][1]

                        
            self.data[node][1] = None

    #[l, l + rangenum)
    def update(self, lft, rangenum, val):
        self.update_range(1, 0, len(self.list_data) - 1, lft, lft + rangenum - 1, val)

    def update_range(self, node, left, right, l, r, val):
        self.propagate(node, left, right)

        #範囲外
        if r < left or right < l:
            return
        #範囲内
        if l <= left and right <= r:
            if self.data[node][1] is None:
                self.data[node][1] = val
            else:
                self.data[node][1] += val
                #if xor
                #self.data[node][1] ^= val
            self.propagate(node, left, right)
            return
        
        #範囲内、範囲外が被っている
        mid = (left + right) // 2
        self.update_range(node * 2, left, mid, l, r, val)
        self.update_range(node * 2 + 1, mid + 1, right, l, r, val)

        self.data[node][0] = self.func(self.data[node * 2][0], self.data[node * 2 + 1][0])

    def query(self, lft, rangenum):
        return self.query_range(1, 0, len(self.list_data) - 1, lft, lft + rangenum - 1)
    
    def query_range(self, node, left, right, l, r):
        # lazy-seg実施
        self.propagate(node, left, right)

        # 範囲外
        if r < left or right < l:
            return self.default

        # 範囲内
        if l <= left and right <= r:
            return self.data[node][0]

        #範囲内、範囲外が被っている
        mid = (left + right) // 2
        left_val = self.query_range(node * 2, left, mid, l, r)
        right_val = self.query_range(node * 2 + 1, mid + 1, right, l, r)
        return self.func(left_val, right_val)
    
    def point_query(self, index):
        return self._point_query(1, 0, len(self.list_data) - 1, index)

    def _point_query(self, node, left, right, index):
        self.propagate(node, left, right)
        if left == right:
            return self.data[node][0]
        mid = (left + right) // 2
        if index <= mid:
            return self._point_query(node * 2, left, mid, index)
        else:
            return self._point_query(node * 2 + 1, mid + 1, right, index)

#input 

a, b, c = map(int, input().split())

for i in range(100):
    aa = a + i
    bb = b + i
    if aa / bb == c:
        print('Yes')
        sys.exit()
print('No')
