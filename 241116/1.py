import sys
input = sys.stdin.readline

num = list(str(input().strip()))

a = num.count("1")
b = num.count("2")
c = num.count("3")

if a == 1 and b == 2 and c == 3:
    print("Yes")
else:
    print("No")
