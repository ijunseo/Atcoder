#基本操作
import sys
input = sys.stdin.readline
from collections import deque
import bisect
import heapq
import math
import copy

#input 
lst = input().rstrip()
llst = input().rstrip()
flag = False
for i in range(len(lst) - len(llst) + 1):
    for j in range(len(llst)):
        now = llst[j]
        if lst[i + j] == now or lst[i + j] == '?':
            if j == len(llst) - 1:
                flag = True
            continue
        else:
            break

print('Yes' if flag else 'No')