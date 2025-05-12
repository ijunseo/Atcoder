#基本操作
import sys
input = sys.stdin.readline

#input 
a, b = map(int, input().split())
st = 1
ans = 0
while st < b:
    st += a - 1
    ans += 1
print(ans)