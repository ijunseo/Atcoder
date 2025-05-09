import sys
input = sys.stdin.readline
num, long = map(int, input().split())
lst = []
for _ in range(num):
    we, lo = map(int, input().split())
    lst.append([we,lo])
for i in range(1, long + 1):
    for j in range(num):
        lst[j][1] += 1
    nowmax = 0
    for j in range(num):
        nowans = lst[j][0] * lst[j][1]
        nowmax = max(nowans, nowmax)
    print(nowmax)