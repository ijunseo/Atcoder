#基本操作
import sys
input = sys.stdin.readline

#input 
n = str(input().rstrip())
lst = []
last = [n[0], 0]
for i in range(len(n)):
    now = n[i]
    if now == last[0]:
        last[1] += 1
    else:
        lst.append(last)
        last = [now, 1]
lst.append(last)

for i in range(len(lst)):
    now = lst[i]
    for j in now:
        print(j, end = '')
print()