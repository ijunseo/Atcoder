import sys
import time
import random
import heapq
from collections import deque, defaultdict

# --------------------------------------------------------------------------------
# 1. 초기화 및 입력 처리
# --------------------------------------------------------------------------------

# 시간을 재기 시작합니다.
START_TIME = time.time()
TIME_LIMIT = 1.85  # 전체 시간 제한 (약간 여유를 둠)
SA_TIME_LIMIT = 0.4  # SA에 사용할 시간

def log(msg):
    # 디버깅용 (채점시에는 무시되거나 주석처리)
    # sys.stderr.write(msg + '\n')
    pass

# 입력 읽기
input_data = sys.stdin.read().split()
iterator = iter(input_data)

try:
    N = int(next(iterator))
    M = int(next(iterator))
    K = int(next(iterator))
    T = int(next(iterator))
except StopIteration:
    # 예외 처리: 데이터가 없는 경우
    sys.exit(0)

adj = [[] for _ in range(N)]
edges = []
for _ in range(M):
    u = int(next(iterator))
    v = int(next(iterator))
    adj[u].append(v)
    adj[v].append(u)
    edges.append((u, v))

# 좌표 정보 (휴리스틱 거리 계산용)
coords = []
for _ in range(N):
    x = int(next(iterator))
    y = int(next(iterator))
    coords.append((x, y))

# --------------------------------------------------------------------------------
# 2. 위상 구조 분석 (Topology Analysis) - 사전 준비
# --------------------------------------------------------------------------------

# 가게: 0 ~ K-1, 나무: K ~ N-1
SHOPS = list(range(K))
TREES = list(range(K, N))

# 거리 계산 (모든 노드 쌍 간 최단 거리 BFS)
# N=100이므로 100번의 BFS는 충분히 빠릅니다.
dist_matrix = [[9999] * N for _ in range(N)]

for start_node in range(N):
    dist_matrix[start_node][start_node] = 0
    q = deque([start_node])
    while q:
        u = q.popleft()
        d = dist_matrix[start_node][u]
        for v in adj[u]:
            if dist_matrix[start_node][v] > d + 1:
                dist_matrix[start_node][v] = d + 1
                q.append(v)

# 간단한 사이클 찾기 (Length 3~5)
# 각 노드에 부착된 곁가지(Detour)를 찾습니다.
# cycles[u] = [[v1, v2], [v3, v4, v5]...] (u에서 시작해서 u로 돌아오는 경로의 중간 노드들)
attached_cycles = defaultdict(list)

def find_cycles():
    for root in range(N):
        # DFS로 짧은 사이클 탐색
        # (curr, start_node, path, length)
        stack = [(root, [root])]
        visited_in_path = {root}
        
        # 반복 없는 단순 DFS (깊이 제한 5)
        # 재귀 대신 스택 사용시 path 관리가 까다로우나 N이 작고 깊이가 얕으므로 재귀 사용 가능
        # 여기서는 간단히 구현
        pass

    # 시간 관계상, 그리고 Python 속도 문제로 완전 탐색보다는
    # "이동 시뮬레이션" 단계에서 즉석으로 찾는 것이 나을 수 있음.
    # 하지만, SA 평가를 위해 미리 "대표적인 척추 경로"는 구해둡니다.
    return

# 가게 간 "척추 경로(Base Route)" 미리 계산
# base_routes[i][j] = [path nodes...]
base_routes = {}
for s1 in SHOPS:
    for s2 in SHOPS:
        if s1 == s2: continue
        # BFS로 경로 복원
        q = deque([[s1]])
        visited = {s1}
        # 최단 경로 하나만 찾음 
        # (BFS 특성상 처음 발견된 경로가 최단)
        while q:
            path = q.popleft()
            u = path[-1]
            if u == s2:
                base_routes[(s1, s2)] = path
                break
            for v in adj[u]:
                if v not in visited:
                    visited.add(v)
                    new_path = list(path)
                    new_path.append(v)
                    q.append(new_path)

# --------------------------------------------------------------------------------
# 3. 지도 최적화 (Simulated Annealing) - 목표 맵 설계
# --------------------------------------------------------------------------------

# 현재 맵의 색상 상태 ('W' or 'R')
# 0: W, 1: R
current_colors = [0] * N  # 0: W, 1: R. 초기: 모두 W
target_colors = [0] * N   # 목표 상태

def evaluate_map(color_config):
    """
    주어진 색상 배치에서 얻을 수 있는 '예상 유니크 문자열 수'를 평가.
    모든 가게 쌍의 최단 경로를 순회하며 만들어지는 문자열을 Set에 넣고 크기 반환.
    """
    generated_strings = set()
    
    # 미리 계산된 척추 경로들만 샘플링하여 빠르게 평가
    # (전체 시뮬레이션은 너무 느림)
    sample_count = 0
    for (s1, s2), path in base_routes.items():
        # 경로를 따라가며 문자열 생성
        s = []
        for node in path:
            if node < K: continue # 가게는 맛이 없음
            # node >= K: 나무
            flavor = 'R' if color_config[node] == 1 else 'W'
            s.append(flavor)
        
        full_str = "".join(s)
        if full_str:
            generated_strings.add(full_str)
        
        # *간단한* 변형 추가: 경로 중간의 노드 하나를 살짝 비틀었다고 가정 (Cycle 효과 근사)
        # R 비중이 적절한지 보기 위함이므로 복잡한 로직 생략
        
    return len(generated_strings)

def run_sa():
    """
    0.4초 동안 SA를 돌려 최적의 R 배치를 찾는다.
    """
    best_config = [0] * N
    best_score = evaluate_map(best_config)
    
    curr_config = list(best_config)
    curr_score = best_score
    
    iters = 0
    
    while time.time() - START_TIME < SA_TIME_LIMIT:
        iters += 1
        # Neighbor: Randomly flip a tree node
        idx = random.choice(TREES)
        
        original_val = curr_config[idx]
        curr_config[idx] = 1 - curr_config[idx] # Flip
        
        new_score = evaluate_map(curr_config)
        
        # Greedy Hill Climbing (SA Temperature 생략 - 단순화)
        if new_score >= curr_score:
            curr_score = new_score
            if new_score > best_score:
                best_score = new_score
                best_config = list(curr_config)
        else:
            # Revert
            curr_config[idx] = original_val
            
    return best_config

# SA 실행 (시간이 없으면 Skip될 수 있도록 안전장치)
if TREES:
    target_colors = run_sa()
else:
    target_colors = [0] * N 

# --------------------------------------------------------------------------------
# 4. 이동 최적화 (Beam Search / Greedy Planner) - 메인 루프
# --------------------------------------------------------------------------------

# 전역 상태
curr_pos = 0
curr_str = ""
delivered_history = [set() for _ in range(K)] # 각 가게별 납품한 문자열 기록
turn_elapsed = 0
real_colors = [0] * N # 실제 환경의 색상 (우리가 바꾼 것 반영)

def get_color(u, colors):
    if u < K: return None
    return 'R' if colors[u] == 1 else 'W'

def solve():
    global curr_pos, curr_str, turn_elapsed, real_colors
    
    # 이전 위치 (바로 되돌아가지 못하게 하기 위함)
    prev_pos = -1 
    
    while turn_elapsed < T:
        remaining_turns = T - turn_elapsed
        
        # -----------------------------------------------
        # Phase 1: 탐색 (Search)
        # 현재 위치에서 이동하여 '새로운 문자열'을 납품할 수 있는
        # 가장 효율적인(가까운) 경로를 찾는다.
        # -----------------------------------------------
        
        found_path = None
        best_path_type = None # 'move' or 'change'
        
        # Dijkstra State: (cost, current_node, current_s, path_history_nodes)
        # path_history_nodes: [next_node, next_next_node, ...] (이동할 경로)
        # 비용: 이동 횟수
        # 목표: 가장 적은 이동으로 `delivered_history`에 없는 문자열을 가게에 배달
        
        # Python 속도 고려: 깊이 제한, 큐 사이즈 제한
        pq = [(0, curr_pos, curr_str, prev_pos, [])] 
        visited_state = set() # (node, string) 방문 체크 (무한 루프 방지)
        
        # 상태 공간이 크므로 visited 관리를 느슨하게 하거나 depth로 제어
        # 'string'이 너무 길어지면 가지치기
        
        search_limit_depth = 12 # 너무 깊게 찾지 않음
        search_count = 0
        max_search_nodes = 800 # 연산량 제한
        
        target_found_cost = 9999
        
        path_candidate = None
        
        while pq:
            cost, u, s, p_node, path = heapq.heappop(pq)
            
            # 탐색 제한
            search_count += 1
            if search_count > max_search_nodes: break
            if cost > search_limit_depth: continue
            
            # 가게 도착 체크
            if u < K: 
                # 시작점이 가게인 경우(Cost 0)는 제외하거나, 빈 문자열이면 무시
                if cost > 0 and s != "":
                    # 중복 확인
                    if s not in delivered_history[u]:
                        # 찾았다!
                        # 하지만 더 짧은 경로가 있을 수 있으니 일단 기록하고 loop 계속?
                        # Dijkstra이므로 처음 나온게 최단 거리임.
                        path_candidate = path
                        target_found_cost = cost
                        break 
                
                # 가게에 도착하면 문자열이 리셋되므로, 여기서 더 이동하는건 
                # 빈 문자열 상태로 이동하는 것과 같음. (연속 납품 가능성)
                # 하지만 이 문제에서는 "가게 도착 -> 납품 -> 리셋"이 강제이므로
                # 여기서 멈추는게 맞음. (더 긴 경로는 의미 없음)
                continue
            
            # 가지치기: 이미 더 긴 비용으로 같은 상태 도달했으면 pass
            state_key = (u, s)
            if state_key in visited_state: continue
            visited_state.add(state_key)
            
            # 이동 (Move)
            for v in adj[u]:
                if v == p_node: continue # 직전 노드로 회귀 불가
                
                # 다음 상태 계산
                next_char = ""
                if v >= K: # 나무
                    next_char = 'R' if real_colors[v] == 1 else 'W'
                
                new_s = s + next_char
                if len(new_s) > 80: continue # 너무 긴 문자열은 효율 떨어짐
                
                heapq.heappush(pq, (cost + 1, v, new_s, u, path + [v]))

        # 탐색 결과 처리
        if path_candidate:
            # 경로가 있으면 이동 수행
            # 첫 번째 이동만 수행하고 다시 평가할지, 쭉 갈지?
            # 여기서는 경로가 "확정된 이득"을 보장하므로 끝까지 수행하는게 효율적일 수 있음.
            # 하지만 중간에 상황이 변하진 않으니, 경로 전체를 명령 큐에 넣고 수행.
            
            # 주의: "경로 전체 수행" 중 T가 끝날 수 있음.
            for next_node in path_candidate:
                if turn_elapsed >= T: break
                
                # 이동 출력
                print(next_node)
                sys.stdout.flush()
                
                # 내부 상태 업데이트
                prev_pos = curr_pos
                curr_pos = next_node
                
                # 문자열 업데이트
                if curr_pos >= K:
                    flavor = 'R' if real_colors[curr_pos] == 1 else 'W'
                    curr_str += flavor
                else:
                    # 가게 도착: 납품
                    if curr_str:
                         # 실제로 새로웠던 것이면 기록 (Set이라 중복 안들어감)
                         delivered_history[curr_pos].add(curr_str)
                    curr_str = "" # 리셋
                
                turn_elapsed += 1
                
        else:
            # -----------------------------------------------
            # Phase 2: 변경 (Modify/Change Flavor)
            # 갈 만한 곳이 없다(탐색 실패/고갈). 맛을 바꿔야 한다.
            # -----------------------------------------------
            
            # 어떤 나무를 바꿀 것인가?
            # 1. Target Map에 'R'로 되어있는데 아직 'W'인 나무 우선
            # 2. 현재 내 위치랑 가까운 곳 우선 (이동 비용 절약)
            # 3. 척추(Backbone) 우선 (ROI 논리)
            
            best_change_node = -1
            best_gain = -1
            
            # 후보군 선정: 전체를 다 보면 느리니, 현재 위치 주변 or 랜덤 샘플링
            # 혹은 Target Map에서 불일치하는 노드들 확인
            
            candidates = []
            
            # 전략 A: Target Map 따르기
            for tree_idx in range(K, N):
                if real_colors[tree_idx] == 0 and target_colors[tree_idx] == 1:
                    candidates.append(tree_idx)
            
            # 만약 Target Map을 다 맞췄거나 후보가 없으면? 
            # -> 아무 W나 R로 바꿔보며 "돌파구"를 찾거나 랜덤 이동
            if not candidates:
                 # 아직 W인 나무들 중 일부를 후보로
                 w_trees = [t for t in TREES if real_colors[t] == 0]
                 if w_trees:
                     candidates = random.sample(w_trees, min(len(w_trees), 5))
            
            if not candidates:
                # 모든 나무가 R이 되었거나 바울 수 없음 -> 랜덤 이동 (Soft Lock 방지)
                # (현실적으로 오면 안되는 상황)
                pass

            # 후보 평가 (간략화된 점수 계산)
            # "이 노드를 바꾸면, 내 위치에서 가까운 가게에 새로운 문자열 배달이 가능한가?"
            # 이걸 시뮬레이션 하긴 무겁다.
            # 휴리스틱: 거리 * (1.0)
            
            # 그냥 가장 가까운 '변경 후보'로 이동해서 바꾸자.
            # (멀리 있는거 바꾸러 가는건 턴 낭비)
            
            candidates.sort(key=lambda x: dist_matrix[curr_pos][x])
            
            target_node = -1
            if candidates:
                target_node = candidates[0]
            
            if target_node != -1:
                # 변경하려는 노드가 현재 위치라면 -> 변경 수행
                if curr_pos == target_node:
                    print("-1") # Change Action
                    sys.stdout.flush()
                    real_colors[curr_pos] = 1 # Update to R
                    turn_elapsed += 1
                    # 문자열에는 영향 없음 (다음 이동 및 도착시 적용, 혹은 현재 위치가 나무라면?)
                    # 문제 정의: "현재 위치가 'W' 나무라면... 'R'로 변경"
                    # 변경 후에는? 코은 변화 없음. 다음 턴 이동시 적용?
                    # 아니, 도착해야 맛을 얻음. 이미 도착해있는 상태에서 바꾸면?
                    # 문제: "나무 도착: ... 끝에 추가됨". "맛 변경: ... 변경".
                    # 이미 서있는 곳의 맛을 바꿔도 내 손의 아이스크림은 안변함.
                else:
                    # 그 노드로 이동해야 함.
                    # 하지만 이동하는 동안에도 "파밍"을 하고 싶음.
                    # Dijkstra가 실패했다는 건 "W로 얻을 게 없다"는 뜻.
                    # 그러니 묵묵히 Target Node로 이동.
                    
                    # 이동 경로 찾기 (BFS)
                    q = deque([(curr_pos, [])])
                    v_set = {curr_pos}
                    move_path = []
                    
                    while q:
                        u, path = q.popleft()
                        if u == target_node:
                            move_path = path
                            break
                        for v in adj[u]:
                            if v not in v_set and v != prev_pos: # 역주행 방지 주의
                                # BFS에서는 path 자체에 역주행이 없지만
                                # 지금 서있는 곳(curr_pos)에서 직전(prev_pos)으로 가는건 막힘
                                # 경로의 첫 스텝이 중요
                                v_set.add(v)
                                q.append((v, path + [v]))
                    
                    if move_path:
                        next_step = move_path[0]
                        print(next_step)
                        sys.stdout.flush()
                        
                        prev_pos = curr_pos
                        curr_pos = next_step
                        if curr_pos >= K:
                            flavor = 'R' if real_colors[curr_pos] == 1 else 'W'
                            curr_str += flavor
                        else:
                            if curr_str: delivered_history[curr_pos].add(curr_str)
                            curr_str = ""
                        turn_elapsed += 1
                    else:
                        # 갈 길을 잃음 (고립?) -> 랜덤 이동
                            available = [v for v in adj[curr_pos] if v != prev_pos]
                            if not available: available = adj[curr_pos] # 막다른 길이면 되돌아가야지...
                            if available:
                                nxt = random.choice(available)
                                print(nxt)
                                sys.stdout.flush()
                                prev_pos = curr_pos
                                curr_pos = nxt
                                if curr_pos >= K:
                                    flavor = 'R' if real_colors[curr_pos] == 1 else 'W'
                                    curr_str += flavor
                                else:
                                    if curr_str: delivered_history[curr_pos].add(curr_str)
                                    curr_str = ""
                                turn_elapsed += 1
            else:
                # 할 게 없다 (랜덤 이동)
                available = [v for v in adj[curr_pos] if v != prev_pos]
                if not available: available = adj[curr_pos]
                if available:
                    nxt = random.choice(available)
                    print(nxt)
                    sys.stdout.flush()
                    prev_pos = curr_pos
                    curr_pos = nxt
                    if curr_pos >= K:
                        flavor = 'R' if real_colors[curr_pos] == 1 else 'W'
                        curr_str += flavor
                    else:
                        if curr_str: delivered_history[curr_pos].add(curr_str)
                        curr_str = ""
                    turn_elapsed += 1

if __name__ == "__main__":
    solve()
