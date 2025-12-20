#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
전체 테스트 케이스에 대해 솔버를 실행하고 점수를 집계하는 스크립트
"""
import subprocess
import os
import glob
from pathlib import Path
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing
import sys

# Windows 인코딩 문제 해결
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def run_solver(input_file, weights=None):
    """
    솔버를 실행하고 결과를 반환
    
    Args:
        input_file: 입력 파일 경로
        weights: 가중치 리스트 (None이면 기본값 사용)
    
    Returns:
        (case_name, score, execution_time) 튜플
    """
    case_name = Path(input_file).stem
    cmd = ['./solver.exe']
    if weights:
        cmd.extend([str(w) for w in weights])
    
    try:
        start = time.time()
        with open(input_file, 'r') as f:
            result = subprocess.run(
                cmd,
                stdin=f,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=120,  # 타임아웃 120초로 증가
                text=True
            )
        elapsed = time.time() - start
        
        if result.returncode == 0:
            score = int(result.stdout.strip())
            return case_name, score, elapsed
        else:
            return case_name, None, elapsed
    except subprocess.TimeoutExpired:
        return case_name, None, 120.0
    except Exception as e:
        return case_name, None, 0.0

def test_all_cases(weights=None, output_file='results.txt', num_workers=None, num_cases=20):
    """
    모든 테스트 케이스에 대해 솔버 실행 (병렬 처리)
    
    Args:
        weights: 가중치 리스트
        output_file: 결과 저장 파일
        num_workers: 병렬 프로세스 수 (None이면 CPU 코어 수)
        num_cases: 사용할 테스트 케이스 수 (기본: 20, 학습시간 15분)
    """
    input_files = sorted(glob.glob('in/*.txt'))[:num_cases]
    
    if not input_files:
        print("Error: in 폴더에 테스트 케이스가 없습니다!")
        return
    
    if num_workers is None:
        num_workers = multiprocessing.cpu_count()
    
    print(f"총 {len(input_files)}개의 테스트 케이스 발견")
    print(f"가중치: {weights if weights else '기본값'}")
    print(f"병렬 프로세스: {num_workers}개 (CPU 코어 활용)")
    print("-" * 60)
    
    results = []
    total_score = 0
    total_time = 0.0
    valid_count = 0
    completed = 0
    
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        future_to_file = {
            executor.submit(run_solver, input_file, weights): input_file 
            for input_file in input_files
        }
        
        for future in as_completed(future_to_file):
            completed += 1
            case_name, score, elapsed = future.result()
            
            if score is not None:
                results.append((case_name, score, elapsed))
                total_score += score
                total_time += elapsed
                valid_count += 1
                print(f"[{completed:3d}/{len(input_files)}] {case_name}: {score:20d} ({elapsed:.2f}s)")
            else:
                results.append((case_name, 0, elapsed))
                print(f"[{completed:3d}/{len(input_files)}] {case_name}: FAILED ({elapsed:.2f}s)")
    
    results.sort(key=lambda x: x[0])
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"가중치: {weights if weights else '기본값'}\n")
        f.write(f"{'케이스':<10} {'점수':>20} {'시간':>10}\n")
        f.write("-" * 45 + "\n")
        
        for case_name, score, elapsed in results:
            f.write(f"{case_name:<10} {score:20d} {elapsed:8.2f}s\n")
        
        f.write("=" * 45 + "\n")
        f.write(f"총점: {total_score}\n")
        f.write(f"평균: {total_score / valid_count if valid_count > 0 else 0:.2f}\n")
        f.write(f"성공: {valid_count}/{len(input_files)}\n")
        f.write(f"총 시간: {total_time:.2f}s\n")
    
    print("=" * 60)
    print(f"Total Score: {total_score}")
    print(f"Average: {total_score / valid_count if valid_count > 0 else 0:.2f}")
    print(f"Success: {valid_count}/{len(input_files)}")
    print(f"Total Time: {total_time:.2f}s")
    print(f"Results saved to {output_file}")
    
    return total_score

if __name__ == '__main__':
    import sys
    
    weights = None
    num_workers = None
    
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == '-j' or sys.argv[i] == '--jobs':
            num_workers = int(sys.argv[i+1])
            i += 2
        else:
            weights = [float(x) for x in sys.argv[i:i+6]]
            break
    
    if weights:
        print(f"사용자 지정 가중치: {weights}")
    else:
        print("기본 가중치 사용")
    
    test_all_cases(weights, num_workers=num_workers)
