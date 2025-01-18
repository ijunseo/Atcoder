import sys
input = sys.stdin.readline
num, cmdnum, nowx, nowy = map(int,input().split())
homelistx = []
homelisty = []
for i in range(num):
    home = list(map(int, input().split()))
    homelistx.append(home)
    homelisty.append([home[1], home[0]])
homelistx.sort(key = lambda x : x[0])
homelisty.sort(key = lambda x : x[0])
cmd = []
for j in range(cmdnum):
    a, b = map(str, input().split())
    b = int(b)
    cmd.append([a, b])
from bisect import *
ans = []
for i in cmd:
    if i[0] == 'R':
        nextx = nowx + i[1]
        bisect_left(lambda x: x = homelistx[x][0])
        nowx = nextx
print(homelistx)
print(homelisty)