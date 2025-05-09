import sys
import math
input = sys.stdin.readline

num = int(input())
for i in range(1, 101):
    num = num // i
    if num == 1:
        print(i)
