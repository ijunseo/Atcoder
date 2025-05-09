import sys
input = sys.stdin.readline
n, m = map(int, input().split())
from collections import defaultdict
import math
rowdict = defaultdict(list)
coldict = defaultdict(list)
rowset = set()
colset = set()
for i in range(m):
    a, b, c = map(str, input().split()) 
    a, b = int(a), int(b)
    rowdict[a].append([b, c])
    coldict[b].append([a, c])
    rowset.add(a)
    colset.add(b)
rowset = sorted(rowset)
colset = sorted(colset)
wmax = math.inf
for i in rowset:
    blow = 0
    for j in rowdict[i]:
        if j[1] == 'B':
            blow = max(blow, j[0])
        else:
            wmax = min(wmax, j[0])
    if blow < wmax:
        continue
    else:
        print('No')
        sys.exit()
wmax1 = math.inf
for i in colset:
    blow1 = 0
    for j in coldict[i]:
        if j[1] == 'B':
            blow1 = max(blow1, j[0])
        else:
            wmax1 = min(wmax1, j[0])
    if blow1 < wmax1:
        continue
    else:
        print('No')
        sys.exit()
print('Yes')