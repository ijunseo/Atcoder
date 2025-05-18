import sys
input = sys.stdin.readline

#input
n = int(input())
lst = list(map(int ,input().split()))

#ボールが入っている段ボールの番号/ setで実装すると探索がO(1)なので計算量的に良いと考えた
ans_set = set([])


#逆順から探索する
#小さい順に見てしまうと、後ろの決定に影響されて複雑になるが、
#大きい番号から見ていけば「後ろの影響を受けずに」順に確定できる
for i in range(n , 0, -1):
    now = lst[i - 1]
    a = 0
    piv = 2
    while i * piv <= n:
        if i * piv in ans_set:
            if not a:
                a = 1
            else:
                a = 0
        piv += 1
    if now == a:
        continue
    else:
        ans_set.add(i)

#output
print(len(ans_set))
print(*ans_set)