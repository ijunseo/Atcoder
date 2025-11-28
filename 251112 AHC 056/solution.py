#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List, Tuple, Dict
import sys
from collections import deque, defaultdict

def read_input():
    it = iter(sys.stdin.buffer.read().split())
    N = int(next(it)); K = int(next(it)); T = int(next(it))
    v = [list(next(it).decode()) for _ in range(N)]       # N x (N-1) horizontal walls
    h = [list(next(it).decode()) for _ in range(N-1)]     # (N-1) x N vertical walls
    targets = [(int(next(it)), int(next(it))) for _ in range(K)]
    return N, K, T, v, h, targets

def neighbors(N:int, v, h, i:int, j:int):
    if i > 0   and h[i-1][j] == '0': yield (i-1, j, 'U')
    if i < N-1 and h[i][j]   == '0': yield (i+1, j, 'D')
    if j > 0   and v[i][j-1] == '0': yield (i, j-1, 'L')
    if j < N-1 and v[i][j]   == '0': yield (i, j+1, 'R')

def bfs_shortest_path(N:int, v, h, start:Tuple[int,int], goal:Tuple[int,int]):
    if start == goal:
        return [start], []
    si, sj = start; gi, gj = goal
    dist = [[-1]*N for _ in range(N)]
    prev = [[(-1,-1)]*N for _ in range(N)]
    prev_dir = [['']*N for _ in range(N)]
    dq = deque([(si, sj)])
    dist[si][sj] = 0
    while dq:
        i, j = dq.popleft()
        for ni, nj, d in neighbors(N, v, h, i, j):
            if dist[ni][nj] != -1: 
                continue
            dist[ni][nj] = dist[i][j] + 1
            prev[ni][nj] = (i, j)
            prev_dir[ni][nj] = d
            if (ni, nj) == (gi, gj):
                dq.clear()
                break
            dq.append((ni, nj))
    if dist[gi][gj] == -1:
        return [start], []
    nodes, dirs = [], []
    cur = (gi, gj)
    while cur != (si, sj):
        nodes.append(cur)
        dirs.append(prev_dir[cur[0]][cur[1]])
        cur = prev[cur[0]][cur[1]]
    nodes.append((si, sj))
    nodes.reverse()
    dirs.reverse()
    return nodes, dirs

def build_route(N:int, v, h, targets:List[Tuple[int,int]]):
    full_nodes = [targets[0]]
    full_dirs: List[str] = []
    for i in range(len(targets)-1):
        a, b = targets[i], targets[i+1]
        nodes, dirs = bfs_shortest_path(N, v, h, a, b)
        full_nodes.extend(nodes[1:])
        full_dirs.extend(dirs)
    return full_nodes, full_dirs  # len(nodes)=X+1, len(dirs)=X

def argmin_C_plus_Q(E:int) -> int:
    """
    E = X+1 (이벤트 수). C in [1..E]에서 C + ceil(E/C) 최소인 C를 반환.
    """
    bestC, bestCost = 1, 10**18
    for C in range(1, E+1):
        Q = (E + C - 1)//C
        cost = C + Q
        if cost < bestCost:
            bestCost = cost
            bestC = C
    return bestC

def main():
    N, K, T, v, h, targets = read_input()

    # 1) 전체 경로
    route_nodes, route_dirs = build_route(N, v, h, targets)
    X = len(route_nodes) - 1
    if X > T:
        # 안전 절단 (이론상 X ≤ T)
        route_nodes = route_nodes[:T+1]
        route_dirs  = route_dirs[:T]
        X = T

    # 2) 이벤트 수
    E = X + 1  # 마지막 도착 이벤트 포함

    # 3) C 최적 선택 & 이벤트 균등 분배(색)
    C = argmin_C_plus_Q(E)
    # 각 이벤트 s의 색: 라운드로빈으로 균등화
    color_of_event = [s % C for s in range(E)]
    # 각 색의 누적 등장 순번 = q 인덱스
    cnt_per_color = [0]*C
    q_of_event = [0]*E
    for s in range(E):
        c = color_of_event[s]
        q_of_event[s] = cnt_per_color[c]
        cnt_per_color[c] += 1
    Q = max(cnt_per_color) if C>0 else 1  # = ceil(E/C)

    # 4) 각 셀의 방문 이벤트 인덱스 목록
    events_of_cell: Dict[Tuple[int,int], List[int]] = defaultdict(list)
    for s in range(E):
        events_of_cell[route_nodes[s]].append(s)

    # 5) 초기 색 격자: 각 셀은 "첫 방문 이벤트의 색"으로 칠한다. (경로 밖은 0)
    s_grid = [[0]*N for _ in range(N)]
    for cell, evs in events_of_cell.items():
        i,j = cell
        s_first = evs[0]
        s_grid[i][j] = color_of_event[s_first]

    # 6) 각 이벤트 s에서 현재 셀을 다음 방문 색으로 재도색(A)
    #    next_color_for_cell_at_event[s] = 해당 셀의 "다음 방문" 색 (없으면 자기색 유지)
    next_color_at_event = [0]*E
    for cell, evs in events_of_cell.items():
        for k, s in enumerate(evs):
            if k+1 < len(evs):
                s_next = evs[k+1]
                next_color_at_event[s] = color_of_event[s_next]
            else:
                # 마지막 방문: 유지
                next_color_at_event[s] = color_of_event[s]

    # 7) 규칙 생성 (s=0..X-1) : (c_s, q_s) → (A=next_color(cell), S=q_{s+1}, D=dirs[s])
    rules = []
    for s in range(X):
        c_in = color_of_event[s]
        q_in = q_of_event[s]
        A_out = next_color_at_event[s]
        S_out = q_of_event[s+1]
        D_out = route_dirs[s]
        rules.append((c_in, q_in, A_out, S_out, D_out))

    # 출력
    out = []
    out.append(f"{C} {Q} {len(rules)}")
    for i in range(N):
        out.append(" ".join(str(s_grid[i][j]) for j in range(N)))
    for (c,q,A,S,D) in rules:
        out.append(f"{c} {q} {A} {S} {D}")
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
