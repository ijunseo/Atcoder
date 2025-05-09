#基本操作
import sys
input = sys.stdin.readline
from collections import defaultdict

dx = [1]
tc = int(input())

for _ in range(tc):
    ans = 0


    n = int(input())
    dic = defaultdict(list)
    lst = list(map(int, input().split()))
    ban_list = []
    for i  in range(2 * n):
        now = lst[i]
        piv = [i - 1, i + 1]
        for j in piv:
            if 0 <=  j < 2 * n:
                pivv = lst[j]
                if now == pivv:
                    ban_list.append(now)



    for i in range(2 * n):
        now = lst[i]
        piv = [i - 1, i + 1]
        for j in piv:
            if 0 <=  j < 2 * n:
                pivv = lst[j]

                if pivv in dic[now]:
                    if pivv in ban_list or now in ban_list:
                        continue
                    ans += 1
                    continue
                dic[now].append(pivv)


    print(ans // 2)
