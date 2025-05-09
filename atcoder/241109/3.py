import sys
a, b = map(int, sys.stdin.readline().split())
rlist = list(map(int, sys.stdin.readline().split()))
rlist.append(a)
numlist = list(map(int, sys.stdin.readline().split()))
num = 0
alllist = [0] * (a + 1)
for i in range(b):
    alllist[rlist[i]] = numlist[i]
for i in range(1, a + 1):
    if alllist[i] != 1:
        

# print(rlist)
# print(numlist)