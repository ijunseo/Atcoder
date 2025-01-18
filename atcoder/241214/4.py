import sys
input = sys.stdin.readline
from bisect import bisect_left
num, ans = map(int, input().split())
numlist = list(map(int,input().split()))
newlist = []
newlist.append(sum(numlist))
newlist1 = []
newlist1.append(sum(numlist))

for i in range(1, num):
    newlist.append(newlist[-1] - numlist[-i])
    newlist1.append(newlist1[-1] - numlist[i - 1])
newlist.append(0)
newlist1.append(0)
newlist1.sort()

maxnum = sum(numlist)
ans1 = ans % maxnum
newans = ans1 + maxnum

def find(a):
    for i in newlist:
        required = a - i
        now = bisect_left(newlist1, required)
        if now < len(newlist1) and newlist1[now] == required:
            return True
    return False

if find(ans1) or find(newans):
    print('Yes')
else:
    print('No')