import sys
input = sys.stdin.readline

n = int(input())

lst = []
for _ in range(n):
    now_num = int(input())
    lst.append(now_num)

s = set()
ans = 0
now = 1

while True:
    if now == 2:
        print(ans)
        sys.exit()

    s.add(now)
    now -= 1
    if lst[now] in s:
        print('-1')
        sys.exit()
    now = lst[now]
    ans += 1

'''
まずボタンを押してから次に光るボタンを保存するリストlstを作成。

例えば、
input = 3, 3, 1, 2なら

lst = [3, 1, 2]で1 -> 3 を押すと２が光る

このシミュレーションを実装するが、サイクル（２番ボタンを押す前にすでに探索した（押した）ボタンに戻ると永遠に２番ボタンを押せないので
ボタンを押した後、次のボタンがすでに確認済みかを確認する必要があるため、set()を用いて確認した。
次は、実装するだけ
'''