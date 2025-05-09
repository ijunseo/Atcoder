changenum = int(input())
str1 = ['0'] + list(map(str, input()))
str2 = ['0'] + list(map(str, input()))
len1 = len(str1)
len2 = len(str2)
anslist = [[0] * (len2) for _ in range(len1)]
for i in range(len2):
    anslist[0][i] = i
for i in range(len1):
    anslist[i][0] = i

for i in range(1, len1):
    for j in range(1, len2):
        if str1[i] == str2[j]:
            anslist[i][j] = anslist[i - 1][j - 1]
        else:
            anslist[i][j] = min(anslist[i - 1][j], anslist[i][j -1], anslist[i - 1][j - 1]) + 1
ans = anslist[-1][-1]

if changenum < ans:
    print('No')
else:
    print('Yes')