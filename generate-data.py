import csv
from collections import Counter
from scipy.stats import betabinom
import numpy as np
import random

# decide how many semi-randomly generated players per strategy
# Gr strategies
num_gr2 = 200
num_gr3 = 300
num_gr4 = 200

# Pr strategies
num_pr1 = 400
num_pr2 = 400

# Blend
num_blend = 3000

# Noise (uniform)
num_random = 0

# this adjusts distributions so that they sum to 100 if needed
def adj(arr):

    rest = 100 - sum(arr)
    if rest > 0:
        while rest >= 0:
            idx = random.randrange(0,9)
            arr[idx] = arr[idx] + 1
            rest = rest - 1
    if rest < 0:
        while rest < 0:
            idx = random.randrange(0,9)
            if arr[idx] > 0:
                A[idx] = arr[idx] - 1
            else:
                idx = arr.index(max(arr))
                arr[idx] = arr[idx] - 1
            rest = rest + 1
    return arr

# PR[1] ----------------------------

# choice of sensible parameters for beta-binomial distribution
param_alpha = [0.45,  0.6, 0.55, 0.50, 0.45, 0.34, 0.33, 0.4, 0.54] 
param_beta = [0.6,  0.94, 0.94,  0.65, 0.65, 0.40, 0.39, 0.41, 0.58]
param = zip(param_alpha, param_beta)
Z = list(param)

N = 100
# lists = sample data collected throughout
lists = []
num = num_pr1

for x in Z:
    t = 0
    # generate beta-binomial samples
    while t < num:
        A = []
        L = list(betabinom.rvs(N, x[0], x[1], size = 90))
        for i in range(N + 1):
            A = np.append(A,(L.count(i)))
        concat = [sum(A[10 * i:10*i+9]) for i in range(10)]
        A = [int(100 * j / sum(concat)) for j in concat]
        #A.append(0)
        for k in [0,1]:
            A[k] = int(100 * concat[k] / sum(concat))
        A[2] = random.randrange(1,15)
        for k in range(3,9):
            A[k] = int(100 * concat[k - 1] / sum(concat))

        # because there are only 10 castles, a natural beta-binomial will produce a conservative approach
        # it forms a good basis though, but requires some adjustment, based on what I would expect a human player to exaggerate
        # what follows are these small adjustments, kept semi-random
        A[3] = A[3] + random.randrange(10,25)
        A[2] = A[2] / (random.randrange(2,3))
        A[0] = A[0] + random.randrange(8,15)
        A[1] = A[1] / random.randrange(2,6)
        A[4] = A[4] + random.randrange(9,17)
        A[8] = A[8] + random.randrange(0,10)
        A[5] = A[5] + random.randrange(5,8)
        if A[9] > 10:
            A[9] = A[9] - random.randrange(5,10)
        if A[0] > 42:
            A[0] = A[0] - random.randrange(2,4)
        if A[2] > 5:
            r = random.randrange(2,5)
            A[5] = A[5] + r
            A[2] = A[2] - r
        if A[7] > 9:
            r = random.randrange(5,9)
            A[7] = A[7] - r
            A[5] = A[5] + r
        if A[3] < 25:
            A[3] = A[3] + random.randrange(8,15)            
        A = [int(100 * j / sum(A)) for j in A]
        if A[1] in [2,3,4]:
            A[3] = A[1] + A[3]
        if A[2] in [2,3,4]:
            A[0] = A[0] + A[2]
        if A[3] < 28:
            if random.randrange(1,10) > 3:
                A[3] = A[3] + 5
        if A[9] > 7:
            if random.randrange(1,10) > 3:
                A[9] = A[9] - 5
                A[5] = A[5] + 5
        A[3] = A[3] + random.randrange(5,9)
        A = adj(A)
        lists.append(A)
        
        t = t + 1

print('Pr[1] done: total is ' + str(len(lists)))

# PR[2] ----------------------------
# comments above apply here as well
A = []

param_alpha = [0.45,  0.6, 0.55, 0.50, 0.45, 0.34, 0.33, 0.4, 0.54] 
param_beta = [0.6,  0.94, 0.94,  0.65, 0.65, 0.40, 0.39, 0.41, 0.58]
param = zip(param_alpha, param_beta)
Z = list(param)

N = 100
num = num_pr2

for x in Z:
    t = 0
    while t < num:
        A = []
        L = list(betabinom.rvs(N, x[0], x[1], size = 90))
        for i in range(N + 1):
            A = np.append(A,(L.count(i)))
        concat = [sum(A[10 * i:10*i+9]) for i in range(10)]
        A = [int(100 * j / sum(concat)) for j in concat]
        for k in [0,1]:
            A[k] = int(100 * concat[k] / sum(concat))
        A[2] = random.randrange(1,15)
        for k in range(3,9):
            A[k] = int(100 * concat[k - 1] / sum(concat))

        A[3] = A[3] + random.randrange(10,25)
        A[2] = A[2] / (random.randrange(2,3))
        A[0] = A[0] - random.randrange(5,10)
        A[1] = A[1] / random.randrange(2,4)
        A[4] = A[4] + random.randrange(9,17)
        A[8] = A[8] + random.randrange(0,10)
        A[5] = A[5] + random.randrange(5,8)
        if A[9] > 10:
            A[9] = A[9] - random.randrange(5,10)
        if A[0] > 42:
            A[0] = A[0] - random.randrange(2,4)
        if A[2] > 5:
            r = random.randrange(2,5)
            A[5] = A[5] + r
            A[2] = A[2] - r
        if A[7] > 9:
            r = random.randrange(5,9)
            A[7] = A[7] - r
            A[5] = A[5] + r
        if A[3] < 25:
            A[3] = A[3] + random.randrange(8,15)            
        A = [int(100 * j / sum(A)) for j in A]
        if A[1] in [2,3,4]:
            A[3] = A[1] + A[3]
        if A[2] in [2,3,4]:
            A[0] = A[0] + A[2]
        if A[3] < 28:
            if random.randrange(1,10) > 3:
                A[3] = A[3] + 5
        if A[9] > 7:
            if random.randrange(1,10) > 3:
                A[9] = A[9] - 5
                A[5] = A[5] + 5

        A = adj(A)           
        lists.append(A)
        
        t = t + 1
        
print('Pr[2] done: total is ' + str(len(lists)))

# GR[2] ----------------------------
# comments as above
A = []

param_alpha = [3.1, 4, 6, 7, 2, 1.9, 1.7, 1.1, 1, 2]
param_beta = [11, 11, 15, 20, 3, 3, 3, 2, 1.8, 2.8]
param = zip(param_alpha, param_beta)
Z = [x for x in param]

N = 100
num = num_gr2


for x in Z:
    t = 0
    while t < num:
        A = []
        L = list(betabinom.rvs(N, x[0], x[1], size = 100))
        for i in range(N + 1):
            A = np.append(A,(L.count(i)))
        concat = [sum(A[10 * i:10*i+9]) for i in range(10)]
        A = concat
        if A[2] < 23:
            A[2] = A[2] + random.randrange(8,12)
        if A[2] > 45:
            A[2] = A[2] - random.randrange(5,10)
        if A[2] < 25:
            A[2] = A[2] + random.randrange(5,10)
        if A[3] <23:
            A[3] = A[3] + random.randrange(8,12)
        if A[3] < 18:
            A[3] = A[3] + random.randrange(5,10)
        if A[0] > random.randrange(7,13):
            A[0] = A[0] - random.randrange(5,7)
        if A[4] < 12:
            A[4] = A[4] + random.randrange(5,15)
        if A[1] < 23:
            A[1] = A[1] + random.randrange(10,15)
        if A[6] > 6:
            A[6] = A[6] - random.randrange(4,7)
        if A[8] >4:
            A[8] = A[8] - random.randrange(2,5)
        if A[5] > 8:
            A[5] = A[5] - random.randrange(0,8)
            A[1] = A[1] + 2
            A[3] = A[3] + 2
                       
        A = [int(100 *j / sum(concat)) for j in concat]
        if A[2] > 45:
            A[2] = 44
        A = adj(A)       
        lists.append(A)
        
        t = t+1

print('Gr[2] done: total is ' + str(len(lists)))

# Gr[3] --------------------
# comments as above

param_alpha = [3.1, 4, 6, 7, 2, 1.9, 1.7, 1.1, 1, 2]
param_beta = [11, 11, 15, 20, 3, 3, 3, 2, 1.8, 2.8]
param = zip(param_alpha, param_beta)

N = 100
Z = [x for x in param]

num = num_gr3

for x in Z:
    t = 0
    while t < num:
        A = []
        L = list(betabinom.rvs(N, x[0], x[1], size = 100))
        for i in range(N + 1):
            A = np.append(A,(L.count(i)))
        concat = [sum(A[10 * i:10*i+9]) for i in range(10)]
        A = concat
        if A[2] < 23:
            A[2] = A[2] + random.randrange(8,12)
        if A[2] > 45:
            A[2] = A[2] - random.randrange(5,10)
        if A[2] < 25:
            A[2] = A[2] + random.randrange(5,10)
        if A[3] <23:
            A[3] = A[3] + random.randrange(8,12)
        if A[3] < 18:
            A[3] = A[3] + random.randrange(5,10)
        if A[0] > random.randrange(7,13):
            A[0] = A[0] - random.randrange(5,7)
        if A[4] < 12:
            A[4] = A[4] + random.randrange(5,15)
        if A[1] < 23:
            A[1] = A[1] + random.randrange(10,15)
        if A[6] > 6:
            A[6] = A[6] - random.randrange(4,7)
        if A[8] >4:
            A[8] = A[8] - random.randrange(2,5)
        if A[5] > 8:
            A[5] = A[5] - random.randrange(0,8)
            A[1] = A[1] + 2
            A[3] = A[3] + 2
                       
        A = [int(100 *j / sum(concat)) for j in concat]
        if A[2] > 45:
            A[2] = 44
        A = adj(A)
        lists.append(A)
        
        t = t+1

print('Gr[3] done: total is ' + str(len(lists)))

# Gr[4] ----------------------

param_alpha = [3.1, 4, 6, 7, 2, 1.9, 1.7, 1.1, 1, 2]
param_beta = [11, 11, 15, 20, 3, 3, 3, 2, 1.8, 2.8]
param = zip(param_alpha, param_beta)

N = 100
Z = [x for x in param]

num = num_gr4

for x in Z:
    t = 0
    while t < num:
        A = []
        L = list(betabinom.rvs(N, x[0], x[1], size = 100))
        for i in range(N + 1):
            A = np.append(A,(L.count(i)))
        concat = [sum(A[10 * i:10*i+9]) for i in range(10)]
        A = concat
        if A[2] < 23:
            A[2] = A[2] + random.randrange(8,12)
        if A[2] > 45:
            A[2] = A[2] - random.randrange(5,10)
        if A[2] < 25:
            A[2] = A[2] + random.randrange(5,10)
        if A[3] <23:
            A[3] = A[3] + random.randrange(8,12)
        if A[3] < 18:
            A[3] = A[3] + random.randrange(5,10)
        if A[0] < random.randrange(0,5):
            A[0] = A[0] + random.randrange(5,7)
        if A[1] < 23:
            A[1] = A[1] + random.randrange(8,12)
        if A[6] > 6:
            A[6] = A[6] - random.randrange(4,7)
        if A[8] >4:
            A[8] = A[8] - random.randrange(2,5)
        if A[5] > 7:
            A[5] = A[5] - random.randrange(2,8)            
        A = [int(100 *j / sum(concat)) for j in concat]
        if A[2] > 45:
            A[2] = 44
        A = adj(A)

        lists.append(A)
        
        t = t+1

print('Gr[4] done: total is ' + str(len(lists)))

# all results without random, for blended strategy
lists_norandom = lists

print('Writing EDGE and GREED to blend CSV...')

file = open('strats.csv','w')
with file :
    writer = csv.writer(file)
    for sol in lists_norandom:
        writer.writerow(sol)

# Blend of Pr and Gr ----------------------------

print('Blending...')

both_strats = []
with open('strats.csv', newline='') as csvfile:
    data = csv.reader(csvfile)
    for d in data:
        H = [int(i) for i in d]
        both_strats.append(H)
  
coords = []
for i in range(10):
    coords.append([both_strats[j][i] for j in range(len(both_strats))])

t = 0
while t < num_blend:
    samp = []
    for k in range(10):
        samp.append(random.choice(coords[k]))
    samp = [round(100*j/sum(samp)) for j in samp]
    samp = adj(samp)
    lists.append(samp)
    t = t + 1
print('Blend done: total is ' + str(len(lists)))

# Random noise (uniform) ------------------------------

t = 0
while t < num_random:
    rnd = []
    for k in range(10):
        rnd.append(random.randrange(10,100))
    rnd = [round(100*j/sum(rnd)) for j in rnd]
    rnd = adj(rnd)
    lists.append(rnd)
    t = t + 1
    print('Random noise done: total is ' + str(len(lists)))

file = open('all-data.csv','w')

with file :
    writer = csv.writer(file)

    for sol in lists:
        writer.writerow(sol)

print('Written so all-data.csv')


