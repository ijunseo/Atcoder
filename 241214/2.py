import sys
input = sys.stdin.readline
num, score = map(int, input().split())

for i in range(num):
    cmd, scr = map(int, input().split())

    if cmd == 1:
        if score < 1600 or 2799 < score:
            continue
        else:
            score += scr
    else:
        if 1200 <= score and score <= 2399:
            score += scr
        else:
            continue
    # if score < 0:
    #     score = 0    
print(score)