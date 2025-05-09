import sys
input = sys.stdin.readline

st = input()
lsta = []
lstb = []
lstc = set()
for i in range(len(st)):
    if st[i] == 'A':
        lsta.append(i + 1)
    elif st[i] == 'B':
        lstb.append(i + 1)
    elif st[i] == 'C':
        lstc.add(i + 1)
ans = 0
for i in range(len(lstb)):
    now = lstb[i]
    for j in lsta:
        if now - j < 0:
            continue
        else:
            if now * 2 - j in lstc:
                ans += 1
print(ans)