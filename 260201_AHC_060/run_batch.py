import os
import sys
import subprocess
import time
import glob
import statistics
import re

# 설정
WORK_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(WORK_DIR, 'input')
OUTPUT_ROOT = os.path.join(WORK_DIR, 'output')

# 실행 시간 폴더 생성
timestamp = time.strftime("%Y%m%d_%H%M%S")
OUTPUT_DIR = os.path.join(OUTPUT_ROOT, timestamp)

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

print(f"Start Batch Processing...")
print(f"Input Directory: {INPUT_DIR}")
print(f"Output Directory: {OUTPUT_DIR}")

# main.py 경로
MAIN_SCRIPT = os.path.join(WORK_DIR, 'main.py')
#MAIN_SCRIPT = os.path.join(WORK_DIR, 'best.py')

# 파일 목록
input_files = sorted(glob.glob(os.path.join(INPUT_DIR, "*.txt")))

scores = []
execution_times = []

for input_file in input_files:
    filename = os.path.basename(input_file)
    output_file = os.path.join(OUTPUT_DIR, filename)
    
    # print(f"Processing {filename}...", end=" ")
    
    start_t = time.time()
    
    # 프로세스 실행
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        # main.py 실행 (stdin을 파일로, stdout을 파일로 연결, stderr 파이프로 캡처)
        result = subprocess.run(
            [sys.executable, MAIN_SCRIPT], 
            stdin=infile, 
            stdout=outfile, 
            stderr=subprocess.PIPE,
            text=True
        )
        
    elapsed = time.time() - start_t
    execution_times.append(elapsed)
    
    # Stderr에서 점수 파싱 ("SCORE: 1234")
    score = 0
    if result.stderr:
        for line in result.stderr.splitlines():
            if "SCORE:" in line:
                try:
                    score = int(line.split("SCORE:")[1].strip())
                except:
                    pass
    
    scores.append(score)
    print(f"[{filename}] Score: {score:>6} | Time: {elapsed:.2f}s")

print("-" * 50)
print("Batch Processing Completed.")
print("-" * 50)

if scores:
    total_score = sum(scores)
    avg_score = statistics.mean(scores)
    max_score = max(scores)
    min_score = min(scores)
    stdev_score = statistics.stdev(scores) if len(scores) > 1 else 0.0
    
    avg_time = statistics.mean(execution_times)
    
    print(f"Total Cases : {len(scores)}")
    print(f"Total Score : {total_score}")
    print(f"Average     : {avg_score:.2f}")
    print(f"Max Score   : {max_score}")
    print(f"Min Score   : {min_score}")
    print(f"Std Dev     : {stdev_score:.2f}")
    print(f"Avg Time    : {avg_time:.2f}s")
else:
    print("No scores recorded.")

print(f"Results saved in: {OUTPUT_DIR}")
