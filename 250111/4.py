# import sys
# input = sys.stdin.readline
# year = int(input())

# lst = list(map(int, input().split()))
# newlist = [0] * len(lst)
# milist = [0] * len(lst)
# for i in range(1, year):
#     if lst[i] >= year - i:
#         newlist[i + 1] += 1
#         lst[i] -= min(year - i, len(lst))
#     else:
#         newlist[i] += 1


#     cnt = 0
#     for j in range(i):
#         if lst[j] != 0:
#             lst[j] -= 1
#             cnt += 1
#     lst[i] += cnt
# print(*lst)

n = int(input())
a = list(map(int, input().split()))

c = [0] * n
d = [0] * (n + 1)

for i in range(n):
    if i != 0:
        c[i] = c[i - 1] + d[i]
        a[i] += c[i]
    print(a)
    print(c)
    print(d)
    print('----------------------------')
    cnt = min(n - i - 1, a[i])
    a[i] -= cnt
    d[i + 1] += 1
    d[min(n, i + cnt + 1)] -= 1

print(" ".join(map(str, a)))
