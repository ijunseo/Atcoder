import sys
input = sys.stdin.readline
from collections import defaultdict
import math

ans = math.inf
dic = defaultdict(list)
dicset = set()
s = set()
n = int(input())
lst = list(map(int, input().split()))
for i in range(n):
    if lst[i] in s:
        dicset.add(lst[i])
        dic[lst[i]].append(i)
    else:
        s.add(lst[i])
        dic[lst[i]].append(i)
for i in dicset:
    l = len(dic[i])
    for j in range(l - 1):
        ans = min(ans, dic[i][j + 1] - dic[i][j] + 1)
print(ans if ans != math.inf else '-1')