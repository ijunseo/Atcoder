import sys
import math
num = int(sys.stdin.readline())
kusa = []
cmdlist = []
ans = 0

for i in range(num):
    try:
        cmd = list(map(int, sys.stdin.readline().split()))
    except:
        cmd = int(sys.stdin.readline())
    cmdlist.append(cmd)

for i in range(num):
    nowcmd = len(cmdlist[i])

    if nowcmd == 1:
        kusa.append(0)

    else:
        cmdnum = cmdlist[i][0]
        cmdans = cmdlist[i][1]
        if cmdnum == 2:
            for j in range(len(kusa)):
                kusa[j] += cmdans

        elif cmdnum == 3:
            for j in range(len(kusa)):
                if kusa[j] >= cmdlist[i][1]:
                    kusa[j] = -math.inf
                    ans += 1
            if ans == 0:
                continue
            else:
                print(ans)
                ans = 0