#基本操作
import sys
input = sys.stdin.readline
from collections import deque
import bisect
import heapq
import math
import copy

#input 
n = int(input())
lst = list(map(int, input().split()))
ans = 0
for i in range(n):
    if not i % 2:
        ans += lst[i]
print(ans)
#solve 
