# These are a few helper functions for the Lecture 1 IPython notebook.

import time, math
from random import choice
import numpy as np

# a few helpful functions
def getDigits(x):  # takes an integer x and returns a list of digits, most significant first
    return [int(a) for a in str(x)]
# 按位还原
def makeInt(digits):  # takes a list of digits (as returned by getDigits) and returns the integer they represent
    return sum([10 ** (len(digits) - i - 1) * digits[i] for i in range(len(digits))])


# multABunch: runs a multiplication function a bunch, and times how long it takes.
#
# Input: myFn: a function which takes as input two n-digit integers
#              (Notice that in python you can pass a function as input!)
#        nVals: list of n values to test at
# Output: lists nValues and tValues so that running myFn on a list of length nValues[i] took (on average over numTrials tests) time tValues[i] milliseconds.
#
# Other optional args:
#    - numTrials: for each n tests, do numTrials tests and average them
#    - listMax: the input lists of length n will have values drawn uniformly at random from range(listMax)
def multABunch(myFn, nVals, numTrials=20):
    nValues = []
    tValues = []
    for n in nVals:
        # run myFn several times and average to get a decent idea.
        runtime = 0
        for t in range(numTrials):
            lst1 = [ choice(range(10)) for i in range(n) ] # generate a random list of length n
            lst2 = [ choice(range(10)) for i in range(n) ] # generate another random list of length n
            X = makeInt(lst1)
            Y = makeInt(lst2)
            start = time.time()
            myFn(X, Y)
            end = time.time()
            runtime += (end - start) * 1000 # measure in milliseconds
        runtime = runtime/numTrials
        nValues.append(n)
        tValues.append(runtime)
    return nValues, tValues

# next, you can do:
# plt.plot(nValues, tValues)
# or something like that

def gradeSchoolMulti(X, Y):
    x = getDigits(X)
    y = getDigits(Y)
    summands = []
    for xD in range(len(x)):
        cur_XD = x[len(x) - xD - 1]  # 按位取X的当前位，从右向左
        #print(cur_XD)
        z = [0 for i in range(xD)]  #
        # print(z)
        carry = 0  # 进位
        for yD in range(len(y)):
            newProd = getDigits(cur_XD * y[len(y) - yD - 1] + carry)
            # print(str(cur_XD) + "*" + str(y[len(y) - yD - 1]) + "=" + str(newProd))
            z.insert(0, newProd[-1])  # 插入末位
            if len(newProd) > 1:  # 有进位
                carry = newProd[0]
            else:
                carry = 0
        z.insert(0, carry)
        summands.append(makeInt(z))
    return sum(summands)

def divide_and_Conque_Multi(X, Y, mode):
    x = getDigits(X)
    y = getDigits(Y)
    return divide_and_Conque_Multi_Recursive(x, y, mode)

def divide_and_Conque_Multi_Recursive(x, y, mode):

    n = max(len(x), len(y))
    while len(x) < n:
        x.insert(0, 0)
    while len(y) < n:
        y.insert(0, 0)

    if n == 1:
        return x[0] * y[0]

    mid = round(n/2)

    a = x[:mid]  # a xhigh
    b = x[mid:]  # b xlow
    c = y[:mid]  # c yhigh
    d = y[mid:]  # d ylow

    if mode == 'triple':  # Toom-Cook
        # high_high = ac
        high_high = divide_and_Conque_Multi_Recursive(a, c, mode)
        # low_low =bd
        low_low = divide_and_Conque_Multi_Recursive(b, d, mode)

        # temp = (a+b) * (c+d) = ac + bc + ad +bd

        temp = divide_and_Conque_Multi_Recursive(getDigits(makeInt(a) + makeInt(b)),  #
                                                 getDigits(makeInt(c) + makeInt(d)), mode)
        # temp = divide_and_Conque_Multi_Recursive([sum(x)], [sum(y)], mode)
        HH = getDigits(high_high) + [0 for i in range(2 * (n - mid))]  # 1, *10^n
        LL = getDigits(low_low)  # 4, *10^0
        TEMP = temp - high_high - low_low  # (a+b)(c+d) - ac - bd
        MID = getDigits(TEMP) + [0 for i in range(n - mid)]  # 2 3, *10^(n/2)


    else:
        high_high = divide_and_Conque_Multi_Recursive(a, c, mode)
        high_low = divide_and_Conque_Multi_Recursive(a, d, mode)
        low_high = divide_and_Conque_Multi_Recursive(b, c, mode)
        low_low = divide_and_Conque_Multi_Recursive(b, d, mode)

        HH = getDigits(high_high) + [0 for i in range(2 * (n - mid))]  # 1, *10^n
        MID = getDigits(high_low + low_high) + [0 for i in range(n - mid)]  # 2 3, *10^(n/2)
        LL = getDigits(low_low)  # 4, *10^0
        # ac * 10^n + (ad + bc) * 10 ^ (n/2) + bd

    return makeInt(HH) + makeInt(MID) + makeInt(LL)



X = 1234567
Y = 654321
times = 1000

#t1, _ = math.modf(time.time())
t1 = time.time()
for i in range(times):
    gradeSchoolMulti(X, Y)
#t2, _ = math.modf(time.time())
t2 = time.time()
for i in range(times):
    divide_and_Conque_Multi(X, Y, '')
t3 = time.time()  #, _ = math.modf(time.time())
for i in range(times):
    divide_and_Conque_Multi(X, Y, 'triple')
t4 = time.time()  #, _ = math.modf(time.time())

print(t2-t1, t3-t2, t4-t3)

