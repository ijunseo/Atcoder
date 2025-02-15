import sys
input = sys.stdin.readline
import math

n = int(input())
st = input()
lst = []
for i in range(n):
    if st[i] == '1':
        lst.append(i + 1)
onelen = len(lst) #1の数
sumlst = sum(lst)

realans = math.inf

for i in range(onelen):
    if i != 0:
        sumlst = sumlst - lst[i - 1] * 2 #abs
    
    l = i 
    r = onelen - 1 - i 
    imsi = (l * (l + 1)) // 2 + (r * (r + 1)) // 2 
    
    ans = -lst[i] * onelen + sumlst + 2 * lst[i] * i #abs
    realans = min(realans, ans - imsi)  
print(realans)