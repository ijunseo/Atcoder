anslist = []
for i in range(1, 10):
    nowlist = []
    for j in range(1 , 10):
        nowlist.append(i * j)
    anslist.append(nowlist)
checknum = int(input())
ans = 0
for i in range(9):
    for j in range(9):
        if anslist[i][j] == checknum:
            ans += checknum
print(2025 - ans)