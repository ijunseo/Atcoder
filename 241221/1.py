import sys
input = sys.stdin.readline
a, b , c = map(int, input().split())
if a == b + c or b == a + c or c == a + b or a == b == c:
    print('Yes')
else:
    print('No')