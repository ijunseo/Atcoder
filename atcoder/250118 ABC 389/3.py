import sys
input = sys.stdin.readline
from collections import deque

ans = deque()
num = int(input())
nowanslist = deque([0])
piv = 0
for _ in range(num):
    try:
        cmd = list(map(int, input().split()))
    except:
        cmd = int(input())

    if cmd[0] == 1:
        ans.append(cmd[1])
        nowanslist.append(nowanslist[-1] + cmd[1])

    elif cmd[0] == 2:
        i = ans.popleft()
        piv += i
        nowanslist.popleft()

    elif cmd[0] == 3:
        newnum = cmd[1]
        print(nowanslist[newnum - 1] - piv)