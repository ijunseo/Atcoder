#基本操作
import sys
input = sys.stdin.readline
from collections import deque
import bisect
import heapq
import math
import copy

#input 
n1 = int(input())
n = str(input().rstrip())
m = str(input().rstrip())
ans = 0
for i in range(n1):
  if n[i] != m[i]:
    ans += 1
print(ans)
#solve 

