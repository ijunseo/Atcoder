import sys
input = sys.stdin.readline

num = int(input())
mx = 0
lst = []
for i in range(num):
    a, b = map(int, input().split())
    mx = max(mx, b)
    

