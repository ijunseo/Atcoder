num = list(map(int, input()))
ans = 0
now = 0
while now < len(num):
    if num[now] != 0:
        ans += 1
        now += 1
    else:
        now += 1
        try:
            if num[now] == 0:
                now += 1
                ans += 1
            else:
                ans += 1
        except:
            ans += 1
print(ans)