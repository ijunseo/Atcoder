import sys
input = sys.stdin.readline
num = int(input())
numlist = list(map(int, input().split()))
numset = set(numlist)
maxanswer = 1
def find(a):
    global maxanswer
    if len(a) == 1:
        return
    if len(a) == 2:
        maxanswer = max(maxanswer, 2)  
    else:
        maxans = 0
        for i in range(len(a)):
            for j in range(i + 1, len(a)):
                ans = 1
                gap = a[j] - a[i]
                now = a[i] + gap
                while now in a:
                    ans += 1
                    now += gap
                maxans = max(ans, maxans)
        maxanswer = max(maxans, maxanswer)  
for i in numset:
    nowlist = []
    for j in range(num):
        if numlist[j] == i:
            nowlist.append(j)
    find(nowlist)
print(maxanswer)