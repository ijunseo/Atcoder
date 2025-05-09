import sys
import itertools

input = sys.stdin.readline

numlist = list(map(int, input().split()))
#print(numlist)
nums = [0, 1, 2, 3, 4]

anslist = []
for k in range(1, 6):
    for i in itertools.combinations(nums, k):
        newlist = []
        for j in i:
            newlist.append(j)
        anslist.append(newlist)

for i in anslist:
    score = 0
    for j in i:
        score += numlist[j]
    i.append(score)
anslist.sort(key = lambda x: x[0])
#print(anslist)
anslist.sort(key = lambda x: x[-1], reverse = True)


reallyanslist = []
for i in anslist:
    lst = []
    for j in i:
        alpha = chr(j + 65)
        lst.append(alpha)
    lst.pop()
    reallyanslist.append(lst)

for i in reallyanslist:
    for j in i:
        print(j, end='')
    print()