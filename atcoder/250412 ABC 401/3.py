#基本操作
import sys
input = sys.stdin.readline
from collections import deque
import bisect
import heapq
import math
import copy

#input 
n, m = map(int, input().split())
fib_lst = [0] * (10 ** 6 + 1)
ans_lst = [0] * (10 ** 6 + 1)

for i in range(m):
    fib_lst[i] = 1
    ans_lst[i] = i + 1
 
for i in range(n - m + 1):
    next = ans_lst[m - 1 + i] * 2
    next -= fib_lst[i]
    fib_lst[m + i] = ans_lst[m - 1 + i] % (10 ** 9)
    ans_lst[m + i] = next % (10 ** 9)

# for i in range(10):
#     print(ans_lst[i])

# for i in range(10):
#     print(fib_lst[i])
if n < m:
    print('1')
    sys.exit()
print(ans_lst[n - 1])