import sys
input = sys.stdin.readline
from collections import defaultdict

n, qnum = map(int, input().split())
dic1 = defaultdict(set)
dic2 = {}
for i in range(1, n + 1):
    dic1[i].add(i)
    dic2[i] = i
for _ in range(qnum):
    lst = list(map(int, input().split()))
    if len(lst) == 3:
        a, b, c = lst
        if a == 1:
            now = dic2[b]
            dic1[now].remove(b)
            dic2[b] = c
            dic1[c].add(b)
        elif a == 2:
            nextset1 = dic1[b]
            nextset2 = dic1[c]
            for i in nextset1:
                dic2[i] = c
            for i in nextset2:
                dic2[i] = b
            dic1[b] = nextset2
            dic1[c] = nextset1

    if len(lst) == 2:
        a, b = lst
        print(dic2[b])