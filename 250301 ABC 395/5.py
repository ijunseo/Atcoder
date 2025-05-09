import sys
input = sys.stdin.readline
import math
import heapq

n, m, x = map(int, input().split())
line1 = [[]for _ in range(2 * n + 1)]
line2 = [[]for _ in range(n + 1)]
for _ in range(m):
    a, b = map(int, input().split())
    line1[a].append(b)
    line1[n + a].append(b)


lenlist = [sys.maxsize] * (n + 1)
lenlist[1] = 0
q = [(0, 1, 0)]
while q:
    nowcost, now, flag = heapq.heappop(q)
    print(now, nowcost, flag)
    if nowcost > lenlist[now]:
        continue
    lenlist[now] = nowcost
    if flag:
        for i in line1[now]:
            if i <= n:
                if lenlist[i] > nowcost + 1:
                    heapq.heappush(q, (nowcost + 1, i, 0))
            else:
                if lenlist[i - n] > nowcost + x +1:
                    heapq.heappush(q, (nowcost + x + 1, i, 1))
    if not flag:
        for i in line1[now]:
            if i <= n:
                if lenlist[i] > nowcost + 1:
                    heapq.heappush(q, (nowcost + 1, i, 0))
            else:
                if lenlist[i - n] > nowcost + x + 1:
                    heapq.heappush(q, (nowcost + x + 1, i, 1))

print(lenlist[-1])
