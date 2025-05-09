import sys
input = sys.stdin.readline

len, str1, str2 = map(str, input().split())
strlist = list(map(str, input().strip()))


for i in range(int(len)):
    if strlist[i] == str1:
        continue
    else:
        strlist[i] = str2
        

for i in strlist:
    print(i, end = '')