#基本操作
import sys
input = sys.stdin.readline
from collections import deque
import bisect
import heapq
import math
import copy

#input 
x, y = map(int, input().split())
lst = [i for i in range(1, 7)]

ans = 0
for i in range(6):
    for j in range(6):
        one = lst[i]
        two = lst[j]
        flag = False
        if one + two >= x:
            ans += 1
            flag = True
        if flag:
            continue
        if abs(one - two) >= y:
            ans += 1

print(ans / 36)


