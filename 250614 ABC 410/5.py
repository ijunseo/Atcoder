#基本操作
import sys
input = sys.stdin.readline

#input 
n,h, m  = map(int, input().split())
dp = [[0 for _ in range(h + 1)] for _ in range(n + 1)]


for i in range(n):
    a, b = map(int, input().split())
    for hp in range(h + 1):
        for mp in range(m + 1):
            if dp[hp][mp] == i:
                if hp >= a:
                    dp[hp - a][mp] = i + 1
                if mp >= b:
                    dp[hp][mp - b] = i + 1

mx = 0
for i in range(h + 1):
    for j in range(m + 1):
        mx = max(mx, dp[i][j])
print(mx)