lst = list(map(int, input().split()))
ans = 0

for i in range(4, 0, -1):
    for j in range(i):
        if lst[j] > lst[j + 1]:
            ans += 1
            lst[j] , lst[j + 1] = lst[j + 1], lst[j]
if ans == 1:
    print('Yes')
else:
    print('No')