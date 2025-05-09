import sys
input = sys.stdin.readline

lst = list(input().split())

if lst[0] == 'sick':
    if lst[1] == 'sick':
        print('1')
    else:
        print('2')
elif lst[0] == 'fine':
    if lst[1] == 'sick':
        print('3')
    else:
        print('4')