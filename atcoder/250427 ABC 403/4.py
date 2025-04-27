#基本操作
import sys
input = sys.stdin.readline
from collections import defaultdict
import bisect
import heapq

#input 
n, m = map(int, input().split())

dic = defaultdict(int)
lst = sorted(list(map(int, input().split())))
lst_set = set(lst)
dx = [-m, m]
llst = []

  

for i in lst_set:
    ans = 0
    numl = bisect.bisect_left(lst ,i)
    numr = bisect.bisect_right(lst, i)
    for j in range(2):
        nxt = i + dx[j]
        if nxt in lst_set:
            lft = bisect.bisect_left(lst ,nxt)
            rgt = bisect.bisect_right(lst, nxt)
            ans += rgt - lft
    if ans:
        llst.append([-ans, i, numr - numl])

realans = 0
heapq.heapify(llst)
while llst:
    now = heapq.heappop(llst)

    now[0] += dic[now[1]]
    now[0] += dic[now[1]]

    for i in range(2):
        dic[now[1] + dx[i]] += now[2]
    if -now[0] >= now[2]:
        realans += now[2]

print(realans)