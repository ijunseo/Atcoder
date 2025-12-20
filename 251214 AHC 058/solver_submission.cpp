#include <iostream>
#include <vector>
#include <array>
#include <algorithm>
#include <cmath>
#include <cstring>
#include <queue>
#include <cassert>
#include <chrono>

using namespace std;
using namespace std::chrono;

// Constants
const int MAX_N = 10;
const int MAX_L = 4;
const int MAX_T = 500;
const int BEAM_WIDTH = 800;  // 공격적 전략
const double TIME_LIMIT = 1.8;  // 시간 제한 (초)

// Global input
int N, L, T;
__int128_t K_init;
array<array<long long, MAX_N>, MAX_L> A_input;
array<array<long long, MAX_N>, MAX_L> C_input;

// 최적 가중치 (Optuna로 찾은 값)
const double BEST_WEIGHTS[6] = {
    0.2074635024729433,  // w1: 현재 사과 수
    3.9441845824540165,  // w2: Level 0 생산력
    2.992649407911294,  // w3: Level 1 기계 파워
    1.5454967711262828,  // w4: Level 2 기계 파워
    1.4952411521259144,  // w5: Level 3 기계 파워
    0.9196082203090659   // w6: 남은 턴 비율
};

// Helper function to print __int128_t
void print_int128(__int128_t x) {
    if (x < 0) {
        cout << '-';
        x = -x;
    }
    if (x == 0) {
        cout << '0';
        return;
    }
    string s;
    while (x > 0) {
        s += char('0' + x % 10);
        x /= 10;
    }
    reverse(s.begin(), s.end());
    cout << s;
}

// Convert __int128_t to double for scoring
double to_double(__int128_t x) {
    if (x == 0) return 0.0;
    double result = 0.0;
    __int128_t temp = x;
    bool negative = false;
    if (temp < 0) {
        negative = true;
        temp = -temp;
    }
    
    if (temp > 1e18) {
        return negative ? -1e100 : 1e100;
    }
    
    result = (double)(long long)temp;
    return negative ? -result : result;
}

// State representation
struct State {
    __int128_t K;
    array<array<__int128_t, MAX_N>, MAX_L> B;
    array<array<long long, MAX_N>, MAX_L> P;
    vector<int> actions;
    double score;
    
    State() : K(0), score(0.0) {
        for (int i = 0; i < MAX_L; i++) {
            for (int j = 0; j < MAX_N; j++) {
                B[i][j] = 0;
                P[i][j] = 0;
            }
        }
    }
};

// Action
struct Action {
    int level;
    int id;
    
    Action(int l = -1, int i = -1) : level(l), id(i) {}
    
    int encode() const {
        if (level == -1) return -1;
        return level * N + id;
    }
    
    static Action decode(int code) {
        if (code == -1) return Action(-1, -1);
        return Action(code / N, code % N);
    }
    
    bool operator<(const Action& other) const {
        if (level != other.level) return level < other.level;
        return id < other.id;
    }
};

// World Model: Deterministic simulation
void advance(State& s, const Action& action) {
    if (action.level != -1) {
        int lv = action.level;
        int id = action.id;
        long long cost = C_input[lv][id] * (s.P[lv][id] + 1);
        
        if (s.K >= cost) {
            s.K -= cost;
            s.P[lv][id]++;
        }
    }
    
    for (int j = 0; j < N; j++) {
        __int128_t production = (__int128_t)A_input[0][j] * s.B[0][j] * s.P[0][j];
        s.K += production;
    }
    
    for (int i = 1; i < L; i++) {
        for (int j = 0; j < N; j++) {
            __int128_t production = s.B[i][j] * s.P[i][j];
            s.B[i-1][j] += production;
        }
    }
}

// Evaluation function with optimized weights
double evaluate(const State& s, int turn) {
    int remaining = T - turn;
    
    __int128_t total_prod_l0 = 0;
    for (int j = 0; j < N; j++) {
        total_prod_l0 += (__int128_t)A_input[0][j] * s.B[0][j] * s.P[0][j];
    }
    
    // 미래 사과 예측 (Greedy Rollout)
    __int128_t future_apples = s.K + total_prod_l0 * remaining;
    
    double f1 = log2(max(1.0, to_double(s.K) + 1.0));
    double f2 = log2(max(1.0, to_double(total_prod_l0) + 1.0));
    
    __int128_t total_l1 = 0;
    for (int j = 0; j < N; j++) {
        total_l1 += s.B[1][j] * s.P[1][j];
    }
    double f3 = log2(max(1.0, to_double(total_l1) + 1.0));
    
    __int128_t total_l2 = 0;
    for (int j = 0; j < N; j++) {
        total_l2 += s.B[2][j] * s.P[2][j];
    }
    double f4 = log2(max(1.0, to_double(total_l2) + 1.0));
    
    __int128_t total_l3 = 0;
    for (int j = 0; j < N; j++) {
        total_l3 += s.B[3][j] * s.P[3][j];
    }
    double f5 = log2(max(1.0, to_double(total_l3) + 1.0));
    
    double f6 = (double)(T - turn) / T;
    
    // 미래 사과 예측 feature
    double f_future = log2(max(1.0, to_double(future_apples) + 1.0));
    
    double score = BEST_WEIGHTS[0] * f1 +
                   BEST_WEIGHTS[1] * f2 +
                   BEST_WEIGHTS[2] * f3 +
                   BEST_WEIGHTS[3] * f4 +
                   BEST_WEIGHTS[4] * f5 +
                   BEST_WEIGHTS[5] * f6 +
                   0.5 * f_future;  // 미래 예측 가중치
    
    return score;
}

// Beam Search
State beam_search() {
    auto start_time = high_resolution_clock::now();
    
    State initial;
    initial.K = K_init;
    for (int i = 0; i < L; i++) {
        for (int j = 0; j < N; j++) {
            initial.B[i][j] = 1;
            initial.P[i][j] = 0;
        }
    }
    
    vector<State> current_beam = {initial};
    State best_state = initial;
    
    for (int turn = 0; turn < T; turn++) {
        // 시간 제한 체크
        auto current_time = high_resolution_clock::now();
        double elapsed = duration_cast<duration<double>>(current_time - start_time).count();
        if (elapsed > TIME_LIMIT) {
            // 시간 초과 시 현재까지의 최선 반환
            break;
        }
        
        vector<State> next_beam;
        
        for (const State& state : current_beam) {
            // ROI 기반 행동 우선순위
            vector<pair<double, Action>> scored_actions;
            
            for (int lv = 0; lv < L; lv++) {
                for (int id = 0; id < N; id++) {
                    long long cost = C_input[lv][id] * (state.P[lv][id] + 1);
                    if (state.K >= cost && cost > 0) {
                        // ROI 계산
                        double gain = 0.0;
                        if (lv == 0) {
                            gain = (double)A_input[0][id] * state.B[0][id] * (T - turn);
                        } else {
                            gain = (double)state.B[lv][id] * pow(10.0, lv) * (T - turn);
                        }
                        double roi = gain / cost;
                        scored_actions.push_back({roi, Action(lv, id)});
                    }
                }
            }
            
            // ROI 내림차순 정렬
            sort(scored_actions.rbegin(), scored_actions.rend());
            
            // Top 15 + nothing 행동만 확장
            vector<Action> possible_actions;
            possible_actions.push_back(Action(-1, -1));  // nothing
            for (int i = 0; i < min(15, (int)scored_actions.size()); i++) {
                possible_actions.push_back(scored_actions[i].second);
            }
            
            for (const Action& action : possible_actions) {
                State next = state;
                next.actions.push_back(action.encode());
                advance(next, action);
                next.score = evaluate(next, turn + 1);
                next_beam.push_back(next);
            }
        }
        
        if (next_beam.size() > BEAM_WIDTH) {
            nth_element(next_beam.begin(), 
                       next_beam.begin() + BEAM_WIDTH, 
                       next_beam.end(),
                       [](const State& a, const State& b) {
                           return a.score > b.score;
                       });
            next_beam.resize(BEAM_WIDTH);
        }
        
        current_beam = move(next_beam);
        if (current_beam.empty()) break;
        
        // 최선 상태 추적
        for (const State& s : current_beam) {
            if (to_double(s.K) > to_double(best_state.K)) {
                best_state = s;
            }
        }
    }
    
    // 마지막 빔에서 최선 찾기
    if (!current_beam.empty()) {
        auto best_it = max_element(current_beam.begin(), current_beam.end(),
                                   [](const State& a, const State& b) {
                                       return to_double(a.K) < to_double(b.K);
                                   });
        if (to_double(best_it->K) > to_double(best_state.K)) {
            best_state = *best_it;
        }
    }
    
    // 행동이 부족하면 -1로 채우기
    while (best_state.actions.size() < T) {
        best_state.actions.push_back(-1);
    }
    
    return best_state;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    
    long long K_temp;
    cin >> N >> L >> T >> K_temp;
    K_init = K_temp;
    
    for (int j = 0; j < N; j++) {
        cin >> A_input[0][j];
    }
    
    for (int i = 0; i < L; i++) {
        for (int j = 0; j < N; j++) {
            cin >> C_input[i][j];
        }
    }
    
    State result = beam_search();
    
    // 행동 시퀀스 출력
    for (int action_code : result.actions) {
        if (action_code == -1) {
            cout << "-1\n";
        } else {
            Action a = Action::decode(action_code);
            cout << a.level << " " << a.id << "\n";
        }
    }
    
    return 0;
}
