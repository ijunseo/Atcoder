import sys
input = sys.stdin.readline
row, col, nowx,nowy = map(int, input().split())
numlist = []
for _ in range(row):
    nowlist = list(map(str, input().strip()))
    numlist.append(nowlist)
at = []
nowx -= 1
nowy -= 1
cmd = list(map(str, input().strip()))
def ishome(a, b):
    global at
    if numlist[a][b] == '@' and [a, b] not in at:
        at.append([a, b])
#print(cmd)
for i in cmd:
    ishome(nowx, nowy)
    #print(nowx + 1, nowy + 1, len(at))
    #print(i)
    if i == 'L':
        if numlist[nowx][nowy - 1] == '#':
            continue
        else:
            nowy -= 1
            ishome(nowx, nowy)
    if i == 'R':
        if numlist[nowx][nowy + 1] == '#':
            continue
        else:
            nowy += 1
            ishome(nowx, nowy)
    if i == 'D':
        if numlist[nowx + 1][nowy] == '#':
            continue
        else:
            nowx += 1
            ishome(nowx, nowy)
    if i ==  'U':
        if numlist[nowx - 1][nowy] == '#':
            continue
        else:
            nowx -= 1
            ishome(nowx, nowy)
print(nowx + 1, nowy + 1, len(at))