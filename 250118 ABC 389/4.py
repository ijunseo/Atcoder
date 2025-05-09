import sys
input = sys.stdin.readline
import math

num = int(input())
pivot = 0.5
ans = 0
firnum = int(math.sqrt(num ** 2 - pivot ** 2) + 0.5)
while True:
    nownum = num ** 2 - pivot ** 2
    if nownum < 0:
        break
    ans +=  int(math.sqrt(nownum) + 0.5)
    pivot += 1
print(ans * 4 - 4 * firnum + 1)