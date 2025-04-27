T = input()
U = input()
if len(T) == 4:
    print("Yes")
else:
    flag = 0
    s = list(set(T) & set(U))
    p = len(s)
    for i in range(len(s)):
        p = U.index(s[i]) if p > U.index(s[i]) else p # 共通部分のUの最初の文字の位置
    s_t = [i for i,x in enumerate(T) if x == U[p]] # TのUとの共通部分の最初の文字の位置のリスト
    for i in s_t:
        flag = 0
        if i - p < 0 or len(U)-p-1 > len(T)-i-1:
            continue
        else:
            for j in range(i-p,i-p+len(U)):
                if T[j] == U[flag] or T[j] == "?":
                    flag += 1
                else:
                    continue     
    if flag == len(U):
        print("Yes")
    else:
        print("No")

