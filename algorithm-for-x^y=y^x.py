# your code goes here
# algo.py: Implementation of Soumava's Algorithm for finding solutions to
#                        x^y = y^x = k
#
# To solve the equation for a given k (e.g. 42), run
#     solve(42)
# Since the solutions are obtained from a converging sequence, to set the number
# of iterations of the sequence that the program checks (e.g. 1000), run
#     solve(42, iters=1000)
#
# This uses the Decimal class for arbitrary-precision arithmetic. To set the
# precision to 30 decimal places, run
#     set_precision(30)
#
# Copyright (C) Shardul C., 2016. You may modify, copy, distribute, or use this
# software for any purpose provided that this copyright notice is preserved.

from math import e, log
from decimal import *

def set_precision(n):
    '''Set the precision of the result to 'n' decimal places.'''
    getcontext().prec = n

def solve(k, iters=500):
    '''Solve 'x^y = y^x = k'. If the 'iters' keyword argument is given, iterate
       the specified number of times (default 500). Solutions are returned as
       Decimal objects.'''
    k = Decimal(str(k))
    x = 0
    if k > e**e:
        # this is a good initial approximation of the smaller solution
        x = Decimal('4.1242') / (k - Decimal('11.787')) + Decimal('1.0193')
    else:
        # this is a good initial approximation of the solution
        x = Decimal('0.5221') * ((k - Decimal('0.4787')).ln()) + Decimal('1.3409')
    y = k**(1 / x)

    for i in range(0, iters):
        x = k**(1/y)
        y = k**(1/x)
    return (x, y)