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
llst = sorted(set(lst), reverse=True)

rank_lst = [0] * n
piv = 1
for i in range(len(llst)):
    pivv = 0
    now = llst[i]
    for j in range(n):
        if lst[j] == now:
            rank_lst[j] = piv
            pivv += 1
    piv += pivv

for i in rank_lst:
    print(i)

