#基本操作
import sys
input = sys.stdin.readline
import bisect
import heapq
import math
import copy

#input 
n, m = map(int, input().split())

ans = set([1])
dotset = set()
parlst = [math.inf] * n
parlst[1] = 1

line = [[]for _ in range(n + 1)]
for _ in range(m):
    a, b = map(int, input().split())
    line[a].append(b)
    line[b].append(a)

def change_par(st, newpar):
    global parlst
    q = [st]
    while q:
        now = q.pop()
        parlst[now] = newpar
        for i in line[now]:
            if parlst[i] > newpar:
                q.append(i)


for i in range(n):
    nowdot = i + 1
    if nowdot in ans:
        ans.remove(nowdot)

        for j in line[nowdot]:
            parlst
            if j in dotset:
                continue
            ans.add(j)
    else:
        need_check.add(nowdot)
        for j in line[nowdot]:
            ans.add(j)
        