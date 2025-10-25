#基本操作
import sys
input = sys.stdin.readline
from collections import deque, defaultdict
import bisect
import heapq
import math
import copy
import math

#input
n, m = map(int, input().split())
line = [[] for _ in range(n + 1)]
for _ in range(m):
    a, b = map(int, input().split())
    line[a].append(b)
    line[b].append(a)

d = input().rstrip()
#print(d)
dic = {}

for i in range(n):
    if d[i] == 'D':
        q = deque([(i + 1, 0)])
        milst = []          # [(dist, nextdot)] 距離昇順・最大2件
        s = set()
        limit = INF
        while q:
            now, cst = q.popleft()
            if cst >= limit:
                continue
            if now in s:
                continue
            s.add(now)

            # S를 만났을 때: 후보 삽입/갱신
            if d[now - 1] == 'S':
                dist = cst
                nextdot = now
                idx = -1
                if len(milst) >= 1 and milst[0][1] == nextdot:
                    idx = 0
                elif len(milst) >= 2 and milst[1][1] == nextdot:
                    idx = 1

                if idx != -1:
                    if dist < milst[idx][0]:
                        milst[idx] = (dist, nextdot)
                        if len(milst) == 2 and milst[0][0] > milst[1][0]:
                            milst[0], milst[1] = milst[1], milst[0]
                else:
                    if len(milst) < 2:
                        milst.append((dist, nextdot))
                        if len(milst) == 2 and milst[0][0] > milst[1][0]:
                            milst[0], milst[1] = milst[1], milst[0]
                    else:
                        if dist < milst[1][0]:
                            milst[1] = (dist, nextdot)
                            if milst[0][0] > milst[1][0]:
                                milst[0], milst[1] = milst[1], milst[0]

                if len(milst) == 2:
                    limit = milst[1][0]

            # dic 재사용: (누적거리 + 저장거리, 저장된 S점)으로 동일하게 삽입/갱신
            if now in dic:
                for dist0, nextdot in dic[now]:
                    dist = cst + dist0
                    idx = -1
                    if len(milst) >= 1 and milst[0][1] == nextdot:
                        idx = 0
                    elif len(milst) >= 2 and milst[1][1] == nextdot:
                        idx = 1

                    if idx != -1:
                        if dist < milst[idx][0]:
                            milst[idx] = (dist, nextdot)
                            if len(milst) == 2 and milst[0][0] > milst[1][0]:
                                milst[0], milst[1] = milst[1], milst[0]
                    else:
                        if len(milst) < 2:
                            milst.append((dist, nextdot))
                            if len(milst) == 2 and milst[0][0] > milst[1][0]:
                                milst[0], milst[1] = milst[1], milst[0]
                        else:
                            if dist < milst[1][0]:
                                milst[1] = (dist, nextdot)
                                if milst[0][0] > milst[1][0]:
                                    milst[0], milst[1] = milst[1], milst[0]

                    if len(milst) == 2 and milst[1][0] < limit:
                        limit = milst[1][0]

            if cst + 1 < limit:
                for nxt in line[now]:
                    q.append((nxt, cst + 1))

        dic[i + 1] = milst
        print(milst[0][0] + milst[1][0])