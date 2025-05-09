import sys
input = sys.stdin.readline
num = list(str(input().strip()))
numlist = []
b = 0
while num:
    a = num.pop()
    if a == '|':
        numlist.append(b)
        b = 0
    else:
        b += 1
numlist.reverse()
numlist.pop()
for i in numlist:
    print(i, end = " ")