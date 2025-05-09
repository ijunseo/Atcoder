#基本操作
import sys
input = sys.stdin.readline
from collections import deque
import bisect
import heapq
import math
import copy

#input 
n, m= map(int, input().split())
par_lst = [i for i in range(n + 1)]

def find(nod):
    if par_lst[nod] != nod:
        return find(par_lst[nod])
    return nod

def union(a, b):
    par_a = find(a)
    par_b = find(b)
    if par_a < par_b:
        par_lst[par_b] = par_a
    else:
        par_lst[par_a] = par_b

line = [0 for _ in range(n + 1)]

for _ in range(m):
    st, ed = map(int, input().split())
    line[st] += 1
    line[ed] += 1
    union(st, ed)

for i in range(1, n + 1):
    if find(i) != 1:
        print('No')
        sys.exit()

for i in range(1, n + 1):
    if line[i] != 2:
        print('No')
        sys.exit()
print('Yes')