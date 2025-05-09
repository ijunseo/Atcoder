import sys
input = sys.stdin.readline
a, b = map(int, input().split())
num = list(str(input().strip()))

last = num[0]
num1 = 0
newlist = []

for i in range(a):

    if last == num[i]:
        num1 += 1
    else:
        newlist.append([num1, last])
        last = num[i]
        num1 = 1
newlist.append([num1, last])
length = len(newlist)
count = 0
for i in range(length):
    if newlist[i][1] == '1':
       count += 1
    if b == count:
        count = i
imsi = newlist[count - 1]
newlist[count - 1] = newlist[count]
newlist[count] = imsi
anslist = []
for i in newlist:
    if i[1] == '0':
        for j in range(i[0]):
            anslist.append(0)
    if i[1] == '1':
        for j in range(i[0]):
             anslist.append(1)
for i in anslist:
    print(i, end = "")
