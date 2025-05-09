import sys
input = sys.stdin.readline
a, b = map(int, input().split())
lst = [True] * (a + 1)
lst1 = list(map(int, input().split()))
for i in lst1:
    lst[i] = False
print(a - b)
for i in range(1, a + 1):
    if lst[i]:
        print(i, end = ' ')