#基本操作
import sys
input = sys.stdin.readline
from collections import deque
import bisect
import heapq
import math
import copy

#input 
n,m  = map(int, input().split())
dp = [math.inf] * (3 ** 10)
mon_lst = list(map(int, input().split()))
animal_lst = [list(map(int, input().split())) for _ in range(m)]

for i in range(3 ** 10):
    

#solve 

