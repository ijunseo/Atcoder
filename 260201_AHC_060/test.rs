use std::cmp::Ordering;
use std::collections::{BinaryHeap, HashMap, HashSet, VecDeque};
use std::io::{self, BufRead};
use std::time::Instant;

// -----------------------------------------------------------------------------
// [설정] 봉인 해제된 파라미터 (Unchained Parameters)
// -----------------------------------------------------------------------------
const TIME_LIMIT_SEC: f64 = 1.95;

// Phase 1: 무한 파밍 (Infinite Farming) 설정
const MAX_SEARCH_NODES: usize = 20_000; 
const DEPTH_LIMIT: usize = 150;          
const STRING_LEN_LIMIT: usize = 200;     

// Phase 2: JIT 시뮬레이션 (Simulation) 설정
const SIMULATION_RANGE: usize = 15;      
const SIMULATION_DEPTH: usize = 40;      
const SIMULATION_NODES: usize = 3000;    

// -----------------------------------------------------------------------------
// Random Number Generator (Xorshift)
// -----------------------------------------------------------------------------
struct Xorshift {
    state: u64,
}

impl Xorshift {
    fn new(seed: u64) -> Self {
        Self {
            state: if seed == 0 { 88172645463325252 } else { seed },
        }
    }
    fn gen_range(&mut self, min: usize, max: usize) -> usize {
        if min >= max { return min; }
        let mut x = self.state;
        x ^= x << 13; x ^= x >> 7; x ^= x << 17;
        self.state = x;
        (x as usize % (max - min)) + min
    }
}

// -----------------------------------------------------------------------------
// Data Structures
// -----------------------------------------------------------------------------
#[derive(Clone, Eq, PartialEq)]
struct State {
    cost: usize,
    u: usize,
    s: Vec<char>,
    path: Vec<usize>, 
}

impl Ord for State {
    fn cmp(&self, other: &Self) -> Ordering {
        other.cost.cmp(&self.cost) // Min-Heap
    }
}

impl PartialOrd for State {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

// -----------------------------------------------------------------------------
// Main Logic
// -----------------------------------------------------------------------------
fn main() {
    let start_time = Instant::now();
    let stdin = io::stdin();
    let mut lines = stdin.lock().lines();

    // 1. 입력 처리
    let line1 = lines.next().unwrap().unwrap();
    let parts: Vec<usize> = line1.split_whitespace().map(|x| x.parse().unwrap()).collect();
    let (n, m, k, t) = (parts[0], parts[1], parts[2], parts[3]);

    let mut adj = vec![vec![]; n];
    for _ in 0..m {
        let line = lines.next().unwrap().unwrap();
        let edge: Vec<usize> = line.split_whitespace().map(|x| x.parse().unwrap()).collect();
        let (u, v) = (edge[0], edge[1]);
        adj[u].push(v);
        adj[v].push(u);
    }

    for _ in 0..n {
        lines.next(); 
    }

    let mut rng = Xorshift::new(20250201);

    // -------------------------------------------------------------------------
    // Solver State
    // -------------------------------------------------------------------------
    let mut curr_pos = 0;
    let mut curr_str = Vec::new();
    let mut delivered_history: Vec<HashSet<Vec<char>>> = vec![HashSet::new(); k];
    let mut turn_elapsed = 0;
    let mut real_colors = vec![0; n]; // 0: W, 1: R (환경)
    let mut last_visited_node = usize::MAX; 

    // 패닉 모드 플래그 (시간 부족 시 활성화)
    let mut panic_mode = false;

    // 메인 루프
    while turn_elapsed < t {
        // Time Check Strategy: 종료 0.15초 전부터는 패닉 모드 전환
        let elapsed_time = start_time.elapsed().as_secs_f64();
        if !panic_mode && elapsed_time > TIME_LIMIT_SEC - 0.15 {
            panic_mode = true;
        }

        // =====================================================================
        // Phase 1: Infinite Farming (BFS/Dijkstra)
        // =====================================================================
        
        let mut farming_path: Option<Vec<usize>> = None;
        let mut found = false;

        // 패닉 모드가 아닐 때만 무거운 탐색 수행
        if !panic_mode {
            let mut pq = BinaryHeap::new();
            pq.push(State { cost: 0, u: curr_pos, s: curr_str.clone(), path: vec![] });

            let mut visited_set: HashSet<(usize, Vec<char>)> = HashSet::new();
            let mut search_cnt = 0;

            while let Some(state) = pq.pop() {
                search_cnt += 1;
                
                // [안전장치] 탐색 중에도 시간이 초과되면 즉시 중단
                if search_cnt % 4096 == 0 {
                    if start_time.elapsed().as_secs_f64() > TIME_LIMIT_SEC - 0.15 {
                        panic_mode = true;
                        break; 
                    }
                }

                if search_cnt > MAX_SEARCH_NODES { break; } 
                if state.cost > DEPTH_LIMIT { continue; }   

                if state.u < k {
                    if state.cost > 0 && !state.s.is_empty() {
                        if !delivered_history[state.u].contains(&state.s) {
                            farming_path = Some(state.path);
                            found = true;
                            break;
                        }
                    }
                    continue; 
                }

                if visited_set.contains(&(state.u, state.s.clone())) { continue; }
                visited_set.insert((state.u, state.s.clone()));

                for &v in &adj[state.u] {
                    // [엄격한 역주행 금지]
                    let actual_prev = if state.path.is_empty() {
                        last_visited_node
                    } else if state.path.len() == 1 {
                        curr_pos
                    } else {
                        state.path[state.path.len()-2]
                    };

                    if v == actual_prev { continue; }

                    let mut next_s = state.s.clone();
                    if v >= k { 
                        let flavor = if real_colors[v] == 1 { 'R' } else { 'W' };
                        next_s.push(flavor);
                    }

                    if next_s.len() > STRING_LEN_LIMIT { continue; }

                    let mut next_path = state.path.clone();
                    next_path.push(v);

                    pq.push(State {
                        cost: state.cost + 1,
                        u: v,
                        s: next_s,
                        path: next_path,
                    });
                }
            }
        }

        if found {
            if let Some(path) = farming_path {
                for next_node in path {
                    if turn_elapsed >= t { break; }
                    println!("{}", next_node);
                    
                    last_visited_node = curr_pos;
                    curr_pos = next_node;

                    if curr_pos >= k {
                        let flavor = if real_colors[curr_pos] == 1 { 'R' } else { 'W' };
                        curr_str.push(flavor);
                    } else {
                        if !curr_str.is_empty() {
                            delivered_history[curr_pos].insert(curr_str.clone());
                        }
                        curr_str.clear();
                    }
                    turn_elapsed += 1;
                }
                continue; 
            }
        }

        // =====================================================================
        // Phase 2: JIT Simulation & Change (Smart Investment)
        // =====================================================================
        
        let mut best_target = usize::MAX;
        let mut best_roi = -1.0;
        let mut change_found = false;

        // 패닉 모드가 아니고 파밍 경로도 없을 때만 시뮬레이션 수행
        if !panic_mode {
            let mut candidates = Vec::new();
            let mut q_cand = VecDeque::new();
            let mut visited_cand = vec![false; n];
            
            q_cand.push_back((curr_pos, 0));
            visited_cand[curr_pos] = true;

            while let Some((u, dist)) = q_cand.pop_front() {
                if dist > SIMULATION_RANGE { break; }
                
                if u >= k && real_colors[u] == 0 { 
                    candidates.push((u, dist));
                }

                for &v in &adj[u] {
                    if !visited_cand[v] {
                        visited_cand[v] = true;
                        q_cand.push_back((v, dist + 1));
                    }
                }
            }

            for (target_u, dist_to_target) in candidates {
                // 시뮬레이션 중 시간 체크
                if start_time.elapsed().as_secs_f64() > TIME_LIMIT_SEC - 0.15 { 
                    panic_mode = true;
                    break; 
                }

                // 가상 변경 (W -> R)
                let original_color = real_colors[target_u];
                real_colors[target_u] = 1;

                let sim_score = simulate_farming_score(
                    n, k, &adj, &real_colors, &delivered_history, 
                    target_u, Vec::new(), 
                    last_visited_node 
                );

                // 원상 복구
                real_colors[target_u] = original_color;

                let investment_cost = dist_to_target + 1; 
                let roi = (sim_score as f64) / (investment_cost as f64);

                if roi > best_roi {
                    best_roi = roi;
                    best_target = target_u;
                }
            }
        }

        if best_target != usize::MAX && best_roi > 0.001 {
            let move_path = get_simple_path(&adj, curr_pos, best_target, last_visited_node);
            if let Some(path) = move_path {
                for next_node in path {
                    if turn_elapsed >= t { break; }
                    println!("{}", next_node);
                    
                    last_visited_node = curr_pos;
                    curr_pos = next_node;

                    if curr_pos >= k {
                        let flavor = if real_colors[curr_pos] == 1 { 'R' } else { 'W' };
                        curr_str.push(flavor);
                    } else {
                        if !curr_str.is_empty() {
                            delivered_history[curr_pos].insert(curr_str.clone());
                        }
                        curr_str.clear();
                    }
                    turn_elapsed += 1;
                }

                if turn_elapsed < t && curr_pos == best_target && real_colors[curr_pos] == 0 {
                    println!("-1");
                    real_colors[curr_pos] = 1; 
                    turn_elapsed += 1;
                }
                continue;
            }
        }

        // =====================================================================
        // Phase 3: Random Walk (Survival / Panic Mode)
        // =====================================================================
        
        let mut valid_neighbors = vec![];
        for &v in &adj[curr_pos] {
            if v != last_visited_node {
                valid_neighbors.push(v);
            }
        }

        if !valid_neighbors.is_empty() {
            let nxt = valid_neighbors[rng.gen_range(0, valid_neighbors.len())];
            if turn_elapsed < t {
                println!("{}", nxt);
                last_visited_node = curr_pos;
                curr_pos = nxt;

                if curr_pos >= k {
                    let flavor = if real_colors[curr_pos] == 1 { 'R' } else { 'W' };
                    curr_str.push(flavor);
                } else {
                    if !curr_str.is_empty() {
                        delivered_history[curr_pos].insert(curr_str.clone());
                    }
                    curr_str.clear();
                }
                turn_elapsed += 1;
            }
        } else {
            // [교착 상태 탈출]
            if turn_elapsed < t {
                if curr_pos >= k && real_colors[curr_pos] == 0 {
                    println!("-1"); 
                    real_colors[curr_pos] = 1;
                    turn_elapsed += 1;
                } else {
                    break;
                }
            } else {
                break;
            }
        }
    }
}

// -----------------------------------------------------------------------------
// Helpers
// -----------------------------------------------------------------------------

fn get_simple_path(adj: &Vec<Vec<usize>>, start: usize, goal: usize, forbidden_prev: usize) -> Option<Vec<usize>> {
    if start == goal { return Some(vec![]); }
    let mut q = VecDeque::new();
    q.push_back((start, vec![]));
    let mut visited = HashSet::new();
    visited.insert(start);

    while let Some((u, path)) = q.pop_front() {
        if u == goal {
            return Some(path);
        }
        for &v in &adj[u] {
            if u == start && v == forbidden_prev { continue; }
            
            if !visited.contains(&v) {
                visited.insert(v);
                let mut new_path = path.clone();
                new_path.push(v);
                q.push_back((v, new_path));
            }
        }
    }
    None
}

fn simulate_farming_score(
    n: usize, k: usize, adj: &Vec<Vec<usize>>, 
    temp_colors: &Vec<i32>, history: &Vec<HashSet<Vec<char>>>,
    start_u: usize, start_s: Vec<char>, prev: usize
) -> usize {
    
    let mut gained_score = 0;
    let mut pq = BinaryHeap::new();
    pq.push(State { cost: 0, u: start_u, s: start_s, path: vec![] });
    
    let mut visited = HashSet::new();
    let mut cnt = 0;

    while let Some(state) = pq.pop() {
        cnt += 1;
        if cnt > SIMULATION_NODES { break; }
        if state.cost > SIMULATION_DEPTH { continue; }

        if state.u < k {
            if state.cost > 0 && !state.s.is_empty() {
                if !history[state.u].contains(&state.s) {
                    gained_score = std::cmp::max(gained_score, state.s.len());
                }
            }
            continue;
        }

        if visited.contains(&(state.u, state.s.clone())) { continue; }
        visited.insert((state.u, state.s.clone()));

        for &v in &adj[state.u] {
            let mut next_s = state.s.clone();
            if v >= k {
                let flavor = if temp_colors[v] == 1 { 'R' } else { 'W' };
                next_s.push(flavor);
            }
            if next_s.len() > 100 { continue; } 

            pq.push(State { cost: state.cost + 1, u: v, s: next_s, path: vec![] });
        }
    }
    gained_score
}