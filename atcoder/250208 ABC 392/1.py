import sys
input = sys.stdin.readline

a, b, c = map(int, input().split())
if c == a * b or b == a * c or a == b * c:
    print('Yes')
else:
    print('No')