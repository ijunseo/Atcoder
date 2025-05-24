#基本操作
import sys
input = sys.stdin.readline
from collections import deque
import bisect
import heapq
import math
import copy

#input 
n = str(input().rstrip())
ans = 0
sub = 0
for i in range(len(n)):
    now = n[-1 - i]
    now = int(now)
    now += 10
    now -= sub
    now %= 10

    sub += now
    sub %= 10
    ans += now + 1
print(ans)