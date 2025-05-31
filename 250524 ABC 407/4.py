#基本操作
import sys
input = sys.stdin.readline

#input 
h, w = map(int, input().split())

lst = [[[0 for _ in range(61)] for _ in range(w)] for _ in range(h)]

for i in range(h):
    llst = list(map(int, input().split()))
    for j in range(w):
        now = llst[j]
        now = str(bin(now))
        for k in range(len(now) - 2):
            nnow = now[- k - 1]
            lst[i][j][k] = int(nnow)

ans_lst = [0 for _ in range(61)]

for i in range(h):
    for j in range(w):
        for k in range(31):
            if lst[i][j][k]:
                ans_lst[k] += 1

#backtrackingdfs
def calc(dots:list):
    nowdots = [i for i in ans_lst]
    for i in dots:
        r = i[0]
        c = i[1]
        for j in range(61):
            if lst[r][c][j]:
                nowdots[j] -= 1
    a = 0
    for i in range(61):
        if nowdots[i] % 2:
            a += 2 ** i
    return a


def bfs(check:list, mxh, mxw):
    #print(check)
    global ans
    nowans = calc(check)
    ans = max(ans, nowans)
    for i in range(h):
        for j in range(w):
            if i < mxh:
                continue
            elif i == mxh:
                if j < mxw:
                    continue
            if (i, j) in check:
                continue
            if j + 1 < w:
                if (i, j + 1) in check:
                    continue

                check.append((i, j))
                check.append((i, j + 1))
                bfs(check, i, j + 1)
                check.pop()
                check.pop()

            if i + 1 < h:
                if (i + 1, j) in check:
                    continue
                check.append((i, j))
                check.append((i + 1, j))
                bfs(check, i, j)
                check.pop()
                check.pop()
                                


ans = 0
check_lst = []
bfs(check_lst, 0, 0)
print(ans)