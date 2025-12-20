#!/usr/bin/env python3
"""
Optuna를 사용한 가중치 자동 최적화 스크립트
"""
import optuna
import subprocess
import json
import os
from datetime import datetime

def objective(trial):
    """
    Optuna 목적 함수: 가중치 조합의 총점을 반환
    
    Args:
        trial: Optuna trial 객체
    
    Returns:
        총점 (최대화 목표)
    """
    # 6개의 가중치 제안
    # w1: 현재 사과 수
    w1 = trial.suggest_float('w1', 0.1, 5.0)
    # w2: Level 0 생산력
    w2 = trial.suggest_float('w2', 0.1, 5.0)
    # w3: Level 1 기계 파워
    w3 = trial.suggest_float('w3', 0.1, 3.0)
    # w4: Level 2 기계 파워
    w4 = trial.suggest_float('w4', 0.1, 2.0)
    # w5: Level 3 기계 파워
    w5 = trial.suggest_float('w5', 0.1, 1.5)
    # w6: 남은 턴 비율
    w6 = trial.suggest_float('w6', 0.0, 1.0)
    
    weights = [w1, w2, w3, w4, w5, w6]
    
    # test_all.py 실행하여 총점 계산
    try:
        # 병렬 trial 실행 시 각 trial이 4개 코어 사용 (20코어 / 5 trials)
        cmd = ['python', 'test_all.py', '--jobs', '4'] + [str(w) for w in weights]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=3600  # 1시간 타임아웃
        )
        
        if result.returncode == 0 and result.stdout:
            # 출력에서 총점 추출
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if 'Total Score:' in line:
                    score_str = line.split(':')[1].strip()
                    score = int(score_str)
                    
                    # 진행 상황 출력
                    print(f"Trial {trial.number}: Score={score:,} | w1={w1:.3f} w2={w2:.3f} w3={w3:.3f} w4={w4:.3f} w5={w5:.3f} w6={w6:.3f}")
                    
                    return score
        
        # stdout가 없거나 Total Score를 찾지 못한 경우
        print(f"Trial {trial.number}: FAILED (no score found)")
        if result.stderr:
            print(f"  Error: {result.stderr[:200]}")
        return 0
        
    except subprocess.TimeoutExpired:
        print(f"Trial {trial.number}: TIMEOUT")
        return 0
    except Exception as e:
        print(f"Trial {trial.number}: ERROR - {e}")
        return 0

def optimize_weights(n_trials=50, n_jobs=5, study_name=None):
    """
    가중치 최적화 실행
    
    Args:
        n_trials: 시도 횟수
        n_jobs: 병렬 작업 수 (1=순차, 기본=5)
        study_name: Study 이름 (재개용)
    """
    # Study 생성 또는 로드
    if study_name is None:
        study_name = f"apple_game_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    storage_name = f"sqlite:///{study_name}.db"
    
    print("=" * 70)
    print(f"🎯 Optuna 가중치 최적화 시작")
    print(f"Study 이름: {study_name}")
    print(f"시도 횟수: {n_trials}")
    print(f"병렬 작업: {n_jobs}")
    print("=" * 70)
    
    study = optuna.create_study(
        study_name=study_name,
        storage=storage_name,
        direction='maximize',
        load_if_exists=True,
        sampler=optuna.samplers.TPESampler(seed=42)
    )
    
    # 최적화 실행
    study.optimize(objective, n_trials=n_trials, n_jobs=n_jobs, show_progress_bar=True)
    
    # 결과 출력
    print("\n" + "=" * 70)
    print("✅ 최적화 완료!")
    print("=" * 70)
    
    best_trial = study.best_trial
    print(f"\n📊 최고 점수: {best_trial.value:,}")
    print(f"\n🎯 최적 가중치:")
    for param, value in best_trial.params.items():
        print(f"  {param}: {value:.4f}")
    
    # 최적 가중치 저장
    best_weights = [
        best_trial.params['w1'],
        best_trial.params['w2'],
        best_trial.params['w3'],
        best_trial.params['w4'],
        best_trial.params['w5'],
        best_trial.params['w6']
    ]
    
    with open('best_weights.json', 'w') as f:
        json.dump({
            'weights': best_weights,
            'score': best_trial.value,
            'trial_number': best_trial.number,
            'timestamp': datetime.now().isoformat()
        }, f, indent=2)
    
    print(f"\n💾 최적 가중치가 best_weights.json에 저장되었습니다.")
    
    # 상위 5개 결과 출력 (pandas 선택)
    try:
        trials_df = study.trials_dataframe()
        top_5 = trials_df.nlargest(5, 'value')[['number', 'value', 'params_w1', 'params_w2', 'params_w3', 'params_w4', 'params_w5', 'params_w6']]
        print(f"\n📈 상위 5개 결과:")
        print(top_5.to_string(index=False))
    except ImportError:
        print(f"\n⚠️  상위 결과 표시를 위해 pandas 설치 권장: pip install pandas")
        # pandas 없이 수동으로 출력
        print(f"\n📈 상위 5개 결과:")
        trials = sorted(study.trials, key=lambda t: t.value if t.value else 0, reverse=True)[:5]
        for i, trial in enumerate(trials):
            print(f"  {i+1}. Trial {trial.number}: Score={trial.value}")
            print(f"     w1={trial.params['w1']:.4f} w2={trial.params['w2']:.4f} w3={trial.params['w3']:.4f}")
            print(f"     w4={trial.params['w4']:.4f} w5={trial.params['w5']:.4f} w6={trial.params['w6']:.4f}")
    
    # 시각화 (옵션)
    try:
        import matplotlib
        matplotlib.use('Agg')  # GUI 없이 저장만
        from optuna.visualization import plot_optimization_history, plot_param_importances
        
        # 최적화 히스토리
        fig1 = plot_optimization_history(study)
        fig1.write_html('optimization_history.html')
        print(f"\n📊 최적화 히스토리: optimization_history.html")
        
        # 파라미터 중요도
        fig2 = plot_param_importances(study)
        fig2.write_html('param_importances.html')
        print(f"📊 파라미터 중요도: param_importances.html")
        
    except ImportError:
        print(f"\n⚠️  시각화를 위해 plotly 설치 권장: pip install plotly")
    
    return best_weights, best_trial.value

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Optuna를 사용한 가중치 최적화')
    parser.add_argument('--trials', type=int, default=80, help='최적화 시도 횟수 (기본: 80)')
    parser.add_argument('--jobs', type=int, default=5, help='병렬 작업 수 (기본: 5)')
    parser.add_argument('--study', type=str, default=None, help='Study 이름 (재개용)')
    parser.add_argument('--resume', action='store_true', help='이전 study 재개')
    
    args = parser.parse_args()
    
    # Study 이름 설정
    study_name = args.study
    if args.resume and study_name is None:
        # 가장 최근 .db 파일 찾기
        import glob
        db_files = glob.glob('apple_game_*.db')
        if db_files:
            study_name = db_files[-1].replace('.db', '')
            print(f"📂 이전 study 재개: {study_name}")
        else:
            print("⚠️  재개할 study를 찾을 수 없습니다. 새로 시작합니다.")
    
    # 최적화 실행
    best_weights, best_score = optimize_weights(
        n_trials=args.trials,
        n_jobs=args.jobs,
        study_name=study_name
    )
    
    # 최적 가중치로 출력 생성 여부 확인
    print("\n" + "=" * 70)
    response = input("최적 가중치로 제출용 출력 파일을 생성하시겠습니까? (y/n): ")
    
    if response.lower() == 'y':
        print("\n🚀 제출용 출력 생성 중...")
        cmd = ['python', 'generate_outputs.py'] + [str(w) for w in best_weights]
        result = subprocess.run(cmd)
        
        if result.returncode == 0:
            print("✅ 출력 파일 생성 완료! (out/ 폴더)")
        else:
            print("❌ 출력 파일 생성 실패")
