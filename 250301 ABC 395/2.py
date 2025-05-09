import sys
input = sys.stdin.readline

n = int(input())
lst = [[] for _ in range(n)]
for i in range(n):
    for j in range(n):
        lst[i].append('#')

for i in range(n):
    j = n - i
    if i <= j:
        if i % 2 == 0:
            for k in range(i, j):
                for h in range(i, j):
                    lst[k][h] = '#'
        if i % 2 == 1:
            for k in range(i, j):
                for h in range(i, j):
                    lst[k][h] = '.'
    else:
        continue
for i in range(n):
    print(''.join(lst[i]))