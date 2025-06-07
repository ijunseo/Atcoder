#基本操作
import sys
input = sys.stdin.readline
from collections import deque
import bisect
import heapq
import math
import copy
import math

#1. ずっとだうん全風rotate
#2. min plus minからプラスまで
#3.ずっとぷらす[1, 2] rotate
#down up
#input 
tc = int(input())

for _ in range(tc):
    n = int(input())
    lst = deque(input().rstrip())
    #print(*lst)
    #print(len(lst))


    if len(lst) == 1:
        print(*lst)

    else:
        s = deque(sorted(lst))

        if lst == s:
            #print('!!')

            print(lst[1], end= '')
            print(lst[0], end= '')
            if len(lst) > 2:
                for j in list(lst)[2:]:
                    print(j, end ='')

        elif lst == deque(reversed(s)):
            lst.rotate(-1)
            for i in lst:
                print(i, end = '')

        else:
            if lst[0] <= lst[1] <= lst[2]:
                for i in list(lst)[:3]:
                    print(i, end = '')
                try:
                    
            dflag = False
            d = 0
            ff = 0

            #uflag = False
            u = None
            for i in range(n - 1):
                now = ord(lst[i])
                nxt = ord(lst[i + 1])
                if now > nxt:
                    if not dflag:
                        dflag = True
                        d = i
                        ff = now
                if dflag:
                    if ff < nxt:#1354 -> 1345, 3212 -> 2123, 5412 -> 4125, 5416
                        u = i
                        #if not uflag:
                            #uflag = True
                            #u = i
                            #break

            if u == None:
                print('!')
                for i in list(lst)[:d]:
                    print(i, end = '')
                lst.rotate(-1)
                for i in list(lst)[d:-1]:
                    print(i, end = '')
                print(lst[0])

            else:
                lllst = deque([])
                for i in range(d, u + 1):
                    lllst.append(lst[i])
                lllst.rotate(-1)
                #print('lllst', lllst)
                for i in list(lllst):
                    print(i, end = '')
                for i in list(lst)[u + 1:]:
                    print(i, end = '')
                print()



           #print(d, u)


        




    # print(lst)
    # if lst == sorted(lst):
    #     for i in lst[:2]:
    #         print(i, end = '')
    #     print(lst[2:])
    # for i in range(n - 1):


