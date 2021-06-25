import csv

# player A (us) against B (opponent); record winner as well as points for each
def match(A,B):
    t = 0
    ptA = []
    ptB = []
    a = 0
    b = 0
    win = 0 # 1 if A, 0 if B
    while t < 10:
        if A[t] > B[t]:
            ptA.append(t+1)
            a = a + 1
            b = 0
        elif B[t] > A[t]:
            ptB.append(t+1)
            b = b + 1
            a = 0
        else:
            a = 0
            b = 0
        if a == 3:
            for i in range(t + 2, 11):
                ptA.append(i)
            if sum(ptA) > sum(ptB):
                win = 1
            return [sum(ptA), w,sum(ptB)]

        if b == 3:
            for i in range(t + 2, 11):
                ptB.append(i)
            if sum(ptA) > sum(ptB):
                win = 1
            return [sum(ptA), w,sum(ptB)]
        t = t + 1
    return [sum(ptA), win ,sum(ptB)]

# load all strats (except uniform)
ALL = []
with open('strats.csv', newline='') as csvfile:
    data = csv.reader(csvfile)
    for d in data:
        H = [int(i) for i in d]
        ALL.append(H)   
M = len(ALL)
SCORES = []
c = 0

# load all data as enemy test list
TESTS = []
with open('all-data.csv', newline='') as csvfile:
    data = csv.reader(csvfile)
    for d in data:
        H = [int(i) for i in d]
        TESTS.append(H)
print('There are ' + str(len(TESTS)) + ' tests')       

# == play-off ==
for x in TESTS:
    score = 0
    wins = 0
    for y in ALL:
        score = score + match(x,y)[0]
        wins = wins + match(x,y)[1]
    c = c  + 1
    if c % 100 == 0:
        print(c)
    SCORES.append([x,round(score / M, 3),round(wins / M * 100, 3)])

# == wins in terms of aggregate score == 
SCORES.sort(key=lambda x:x[1])
print('According to scores:')
# top 10
for s in SCORES[-10:]:
    print(s)

# == wins in terms of number of wins ==
SCORES.sort(key=lambda x:x[2])

print('According to wins:')
# top 10
for s in SCORES[-10:]:
    print(s)
