import sys
input = sys.stdin.readline

n = int(input())
lst = list(map(int, input().split()))
for i in range(n - 1):
    if lst[i] < lst[i + 1]:
        continue
    else:
        print('No')
        sys.exit()
print('Yes')