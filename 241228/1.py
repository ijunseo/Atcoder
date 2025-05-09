num = list(map(int,input().split()))
numset = set(num)
if len(numset) == 2:
    print('Yes')
else:
    print('No')