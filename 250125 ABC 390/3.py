import sys
input = sys.stdin.readline

row, col = map(int, input().split())
lst = [list(map(str,input().rstrip())) for _ in range(row)]
minmaxlst = []
black = []
blackhatena = []
for i in range(row):
    kurolst = []
    kurohatena = []
    for j in range(col):
        if lst[i][j] == '#' or lst[i][j] == '?':
            kurohatena.append(j)
            if lst[i][j] == '#':
                kurolst.append(j)
        
    black.append(kurolst)
    blackhatena.append(kurohatena)
checklist = []
for i in range(row):
    if len(black[i]) != 0:
        checklist.append(i)


recheck = [-1, 1000000]
for i in checklist:
    now = list(blackhatena[i])
    mi = now[0]
    ma = now[-1]
    recheck[0] = max(recheck[0], mi)
    recheck[1] = min(recheck[1], ma)

for i in range(row):
    for j in black[i]:
        if  recheck[0] > j or j > recheck[1]:
            print('No')
            sys.exit()
print('Yes')