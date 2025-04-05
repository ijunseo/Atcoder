#基本操作
import sys
input = sys.stdin.readline

#input 
n, m =map(int, input().split())
lst = [list(input().rstrip()) for _ in range(n)]

st_c, st_r, ed_c, ed_r = map(int, input().split())
st = [st_c - 1, st_r - 1]
ed = [ed_c - 1, ed_r - 1]

dx = [1, -1, 0, 0]
dy = [0, 0, 1, -1]

def search(_q):
    map_lst = [[0] * m for _ in range(n)]
    search_lst = []
    while _q:
        now_c, now_r = _q.pop()
        if map_lst[now_c][now_r]:
            continue
        search_lst.append([now_c, now_r])
        if now_c == ed[0] and now_r == ed[1]:
            print(ans)
            sys.exit()

        if map_lst[now_c][now_r]:
            continue
        map_lst[now_c][now_r] = 1
        for i in range(4):
            next_c = now_c + dx[i]
            next_r = now_r + dy[i]
            if 0 <= next_c < n and 0 <= next_r < m:
                if lst[next_c][next_r] == '#':
                    continue
                if not map_lst[next_c][next_r]:
                    _q.append([next_c, next_r])
    return search_lst

ans = 0
while True:
    nowlst = search([st])
    ans += 1
    newlst = []
    for now_c, now_r in nowlst:
        for i in range(4):
            next_c = now_c + dx[i]
            next_r = now_r + dy[i]
            if 0 <= next_c < n and 0 <= next_r < m:
                if lst[next_c][next_r] == '#':
                    newlst.append([next_c, next_r])
                    next_c += dx[i]
                    next_r += dy[i]
                    if 0 <= next_c < n and 0 <= next_r < m:
                        if lst[next_c][next_r] == '#':
                            newlst.append([next_c, next_r])
                else:
                    continue
    for i in newlst:
        lst[i[0]][i[1]] = '.'