#基本操作
import sys
input = sys.stdin.readline
from collections import deque
import bisect
import heapq
import math
import copy

#input 
n = input().rstrip()
alpha_list = set(['a', 'b', 'c', 'd', 'e', 'f', 'g',  'h', 'i', 'j' ,'k' ,'l', 'm', 'n', 'o', 'p', 'q', 'r' ,'s' ,'t' ,'u' ,'v', 'w' ,'x' ,'y' ,'z'])
for i in range(len(n)):
    now = n[i]
    if now in alpha_list:
        alpha_list.remove(now)
print(list(alpha_list)[0])
#solve 

