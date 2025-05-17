import sys
input = sys.stdin.readline

n = int(input())

lst = []
for _ in range(n):
    now_num = int(input())
    lst.append(now_num)

s = set()
ans = 0
now = 1

while True:
    if now == 2:
        print(ans)
        sys.exit()

    s.add(now)
    now -= 1
    if lst[now] in s:
        print('-1')
        sys.exit()
    now = lst[now]
    ans += 1