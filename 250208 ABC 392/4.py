import sys
input = sys.stdin.readline
from collections import deque
import bisect

n = int(input())
lst = []
nlst = []
nnlst = []
for _ in range(n):
    now = deque(map(int, input().split()))
    a = now.popleft()
    nlst.append(a)
    a = sorted(now)
    lst.append(a)
    nnlst.append(sorted(set(a)))


ans = 0
for i in range(n - 1):
    for j in range(i + 1, n):
        now = nnlst[i]
        s = nlst[i] * nlst[j]
        nowans = 0
        for k in now:
            l1 = bisect.bisect_left(lst[i], k)
            r1 = bisect.bisect_right(lst[i], k)
            num1 = r1 - l1
            l2 = bisect.bisect_left(lst[j], k)
            r2 = bisect.bisect_right(lst[j], k)
            num2 = r2 - l2
            nowans += (num1 * num2) / s
        ans = max(ans, nowans)


print(ans)