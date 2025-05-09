lst = list(map(int, input().split()))
a = 0
for i in range(4):
    if lst[i] > lst[i + 1]:
        a += 1

if a == 1:
    print('Yes')
else:
    print('No')