import sys
num = int(sys.stdin.readline())
numlist = list(str(sys.stdin.readline().strip('\n')))
ans = 0
ansnum = ""
for i in range(num):
    ansnum += numlist[i]
    ansnum1 = int(ansnum)
    ans += ansnum1
    print(ansnum)
for i in range(num - 1):
    ansnum = ansnum[1:]
    ansnum1 = int(ansnum)
    ans += ansnum1
    print(ansnum)
print(ans)
