#!/usr/bin/env python3
"""
모든 테스트 케이스에 대해 출력 파일을 생성하는 스크립트
"""
import subprocess
import os
import glob
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing

def generate_output(input_file, weights=None):
    """
    단일 테스트 케이스에 대한 출력 생성
    
    Args:
        input_file: 입력 파일 경로
        weights: 가중치 리스트
    
    Returns:
        (case_name, success, message) 튜플
    """
    case_name = Path(input_file).stem
    output_file = f"out/{case_name}.txt"
    
    cmd = ['./solver.exe', '--output-actions']
    if weights:
        cmd.extend([str(w) for w in weights])
    
    try:
        with open(input_file, 'r') as fin:
            with open(output_file, 'w') as fout:
                result = subprocess.run(
                    cmd,
                    stdin=fin,
                    stdout=fout,
                    stderr=subprocess.PIPE,
                    timeout=120,
                    text=True
                )
        
        if result.returncode == 0:
            return case_name, True, "성공"
        else:
            return case_name, False, f"오류: {result.stderr[:100]}"
    except subprocess.TimeoutExpired:
        return case_name, False, "타임아웃"
    except Exception as e:
        return case_name, False, f"예외: {str(e)[:100]}"

def generate_all_outputs(weights=None, num_workers=None):
    """
    모든 테스트 케이스에 대해 출력 생성 (병렬 처리)
    
    Args:
        weights: 가중치 리스트
        num_workers: 병렬 프로세스 수
    """
    # out 폴더 생성
    os.makedirs('out', exist_ok=True)
    
    # 입력 파일 찾기
    input_files = sorted(glob.glob('in/*.txt'))
    
    if not input_files:
        print("Error: in 폴더에 테스트 케이스가 없습니다!")
        return
    
    if num_workers is None:
        num_workers = multiprocessing.cpu_count()
    
    print(f"총 {len(input_files)}개의 출력 파일 생성 시작")
    print(f"가중치: {weights if weights else '기본값'}")
    print(f"병렬 프로세스: {num_workers}개")
    print("-" * 60)
    
    success_count = 0
    completed = 0
    
    # 병렬 실행
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        future_to_file = {
            executor.submit(generate_output, input_file, weights): input_file 
            for input_file in input_files
        }
        
        for future in as_completed(future_to_file):
            completed += 1
            case_name, success, message = future.result()
            
            if success:
                success_count += 1
                print(f"[{completed:3d}/{len(input_files)}] {case_name}: ✓ {message}")
            else:
                print(f"[{completed:3d}/{len(input_files)}] {case_name}: ✗ {message}")
    
    # 요약
    print("=" * 60)
    print(f"생성 완료: {success_count}/{len(input_files)}")
    print(f"출력 파일 위치: out/")
    
    return success_count

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
    
    generate_all_outputs(weights, num_workers=num_workers)
