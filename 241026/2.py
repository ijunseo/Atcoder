list1 = []
for i in range(8):
    list2 = list(map(str, input()))
    list1.append(list2)
answerlist = []
def find(a):
    global answerlist
    for i in range(8):
        if a[i] == "#":
            answerlist.append(i)
        else:
            continue
    for j in range(8):
        if a[j] == "#":
            break
        else:
            continue
    answerlist.append("x")
for i in range(8):
    find(list1[i])
print(answerlist)
num = 0
for i in range(8):
    if answerlist[i] == "x":
        answerlist[i] = 10
        num += 1
print(num)
answerlistset = set(answerlist)
print(answerlistset)
num1 = 8
for i in range(8):
    if i in answerlistset:
        num1 -= 1
print(num1)
print(num * num1)
