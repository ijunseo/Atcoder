import bisect
import sys
input = sys.stdin.readline
num = int(input())
lst = list(map(int, input().split()))
lastnum = lst[-1]
cnt = 0
for i in range(num):
    pivot = lst[i] * 2
    if pivot > lastnum:
        print(cnt)
        sys.exit()
    else:
        ans = bisect.bisect_left(lst, pivot)
        cnt += len(lst) - ans