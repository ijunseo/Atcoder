import sys
input = sys.stdin.readline

n = int(input())

lst = list(map(int, input().split()))
for i in range(n - 2):
    if lst[i + 1] ** 2 != lst[i] * lst[i + 2]:
        print('No')
        sys.exit()
print('Yes')