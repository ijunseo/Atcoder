#input 
n = int(input())
for _ in range(n):
    m = int(input())
    lst = list(map(int, input().split()))
    lst.sort(key = lambda x : abs(x), reverse= True)
    flag = True
    s = set(lst)
    ss = list(s)
    if len(ss) == 2:
        if ss[0] == -ss[1]:
            print('Yes')
            continue

    print('Yes')