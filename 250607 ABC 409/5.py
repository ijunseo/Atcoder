T = int(input())
res = []

for _ in range(T):
    N = int(input())
    S = input()
    
    min_str = S  # 아무것도 안 바꾼 경우 포함됨
    
    for l in range(N):
        if l == N-1:
            rotated = S
        else:
            rotated = S[:l] + S[l+1:] + S[l]
        
        if rotated < min_str:
            min_str = rotated

    res.append(min_str)

print('\n'.join(res))
