#基本操作
import sys
input = sys.stdin.readline
from collections import defaultdict
import bisect
import heapq
import math
import copy

#input 
n, m, q = map(int, input().split())

dic = defaultdict(set)
for _ in range(q):
    cmd = list(map(int, input().split()))
    if cmd[0] == 1:
        dic[cmd[1]].add(cmd[2])
    elif cmd[0] == 2:
        dic[cmd[1]].add(0)
    else:
        if 0 in dic[cmd[1]]:
            print('Yes')
        else:
            if cmd[2] in dic[cmd[1]]:
                print('Yes')
            else:
                print('No')

#solve 



