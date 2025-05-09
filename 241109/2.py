import sys
a, b = map(int,sys.stdin.readline().split())
tooth = list(str(sys.stdin.readline().strip()))
ans = 0
c = 0
for i in range(len(tooth)):
    if tooth[i] == "O":
        c += 1
    if tooth[i] == "X":
        c = 0
    if c == b:
        ans += 1
        c = 0
print(ans)