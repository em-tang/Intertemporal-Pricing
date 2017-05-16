import random
import itertools
import numpy as np

#Tunable parameters
prices = [1,2,3,4,5]   # A list of possible prices we can charge
mass = [1, 1, 1, 1]    # A list of arrival masses for each customer type [0 periods, 1 period,...]
S = len(mass)-1        # The maximum number of periods our customer base is willing to wait
cycle = 2*S            # The maximum possible length of a single cycle
pSeq = [[0]*(t) for t in range(cycle+1)] # the optimal price sequence

#initialize matrix W of dimensions (p,t)
W = [[0]*len(prices) for t in range(cycle)]
#store optimal price and period k for each W_n(p) for each time horizon with lowest price p
KWnp = [[0]*len(prices) for t in range(cycle)]
PWnp = [[0]*len(prices) for t in range(cycle)]

# The cdf for the demand function as a function of price p and the number of periods w that a given 
# customer type is willing to wait. In this case, it is a simple binary function of
def cdf(w, p):
	if prices[p] > (5 - w):
		return 1
	else: 
		return 0

# number of arrivals for a consumer type in the cycle
def findArrivals(n, k, w):
	temp = max(min(k, n-w) - max(1, k-w) + 1,0)
	return temp

def valueFn(k,p,n):
	val = 0
	for w in range(len(mass)):
		val = val + findArrivals(n,k,w)*mass[w]*prices[p]*(1 - cdf(w, p))
	val = val + W[k-1][p] + W[n-k][p]
	return val

# maximum given the cycle length and minumum price
def findValue(n,index):
    curr_max = 0
    curr_p = 0
    curr_k = 0
    for p in range(index,len(prices)):
        for k in range(1,n+1):
            curr_val = valueFn(k,p,n)
            if curr_max <= curr_val:
                curr_max = curr_val
                curr_p = p
                curr_k = k
    return [curr_max, curr_k, curr_p]

def findValueAgain(p, T):
	rev = 0
	for w in range(len(mass)):
		rev = rev + min(w+1, T)*mass[w]*prices[p]*(1-cdf(w,p)) 
	rev = rev + W[T-1][p]
	return rev

# iteratively calculate each value of matrix
for row in range(1,cycle):
    for index in range(len(prices)):
        #store the maximum revenue given cycle length and minimum price,
        #and the corresponding optimal second lowest price and which period to charge it at
        result = findValue(row, index)
        W[row][index] = result[0]
        KWnp[row][index] = result[1]
        PWnp[row][index] = result[2]

# find number of periods and price sequence
# determine the optimal price sequence
# the start is the start of the period for which we want to know the price
# the end is the end of that period 
# prcyc -- the price cycle array, prcyc[i] is the ith price to charge (ignores
# entry prcyc[0]) -- note that this function returns the index of the price
# in the price list rather than price itself
def priceSeq(start,end,prcyc):
    # base case -- when start == end we are considering a one period problem
    if start == end:
        p = PWnp[1][prcyc[end+1]]
        prcyc[end] = p
        return
    if end < start:
        return
    
    # otherwise, determine the price to charge each period
    n = end - start + 1 # length of the period
    k = KWnp[n][prcyc[end+1]]
    p = PWnp[n][prcyc[end+1]]
    prcyc[start+k-1] = p

    priceSeq(start,start + k-2,prcyc)
    priceSeq(start+k,end,prcyc)
    return


best_prices = [0]*(cycle)
# best average revenues
best_revenues = [0]* len(best_prices)
max_revs = [0]* len(best_prices)
for T in range(1, cycle+1):
    max_p = 0
    max_rev = 0
    for p in range(len(prices)):
        print("Testing price", prices[p])
        rev = findValueAgain(p, T)
        print("Revenue at this price:",rev)
        if max_rev <= rev: 
            max_p = p
            max_rev = rev
    
    # compute the optimal price cycle for a policy of length T
    temp = [0]*(T+1)
    temp[T] = max_p
    priceSeq(1,T-1,temp)
    pSeq[T] = temp

    best_prices[T-1] = prices[max_p]
    best_revenues[T-1] = float( max_rev )/ T
    max_revs[T-1] = max_rev



