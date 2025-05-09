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
ans = 0
flag = False

for _ in range(n):
    cmd = str(input().rstrip())
    if cmd == 'login':
        flag = True
    if cmd == 'logout':
        flag = False
    if cmd == 'private':
        if not flag:
            ans += 1
print(ans)