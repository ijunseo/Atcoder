import sys
input = sys.stdin.readline

d = {}
n = int(input())
a = list(map(int, input().split()))
b = list(map(int, input().split()))
for i in range(n):
    now = b[i]
    d[now] = a[i]
for i in range(1, n + 1):
    watch = d[i]
    print(b[watch - 1], end = ' ')