import sys
input = sys.stdin.readline

n, m = map(int, input().split())

line = [set() for _ in range (n + 1)]

ans = 0
for _ in range(m):
    a, b = map(int, input().split())
    if a == b:
        ans += 1
    else:
        if b in line[a]:
            ans += 1
            continue
        line[a].add(b)
        line[b].add(a)

print(ans)