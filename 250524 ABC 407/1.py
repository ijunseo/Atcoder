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
ans = n/m
print(round(ans))

