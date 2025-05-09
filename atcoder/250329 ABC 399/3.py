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
line = [[] for _ in range(n + 1)]

ans = 0
wentlst = [False] * (n + 1)

q = deque([])

lst = set()
for i in range(m):
    a, b = map(int, input().split())
    line[a].append(b)
    line[b].append(a)
    lst.add(a)
    lst.add(b)

lst = deque(lst)


while lst:
    now = lst.pop()
    wentlst[now] = True
    for i in line[now]:
        if not wentlst[i]:
            wentlst[i] = True
            ans += 1
            lst.append(i)

print(m - ans)
