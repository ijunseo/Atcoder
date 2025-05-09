#基本操作
import sys
input = sys.stdin.readline
from collections import deque
import bisect
import heapq
import math
import copy

#input 
n = map(int, input().split())
n_1 = int(math.sqrt(n))
print
ans = 0
for i in range (m + 1):
    ans += n ** i
    if ans > 10 ** 9:
        print('inf')
        sys.exit()
print(ans)
#solve 

