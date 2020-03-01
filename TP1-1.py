import numpy as np
import scipy.optimize as sco
import matplotlib.pyplot as plt
import time


#______Klee-Minty LP
n = [i for i in range(2, 20)]
dT = []
res = []

for i in n :
    A = np.zeros((i, i))
    b = []
    c = []
    for j in range(i):
        for k in range(i):
            if k == j :
                A[k, k] = 1
            else :
                A[j, k] = (2 * 10 ** (j - k))
        c.append(-10 ** (i - j))
        b.append(100 ** j)
    A = np.tril(A)
    t0 = time.process_time()
    res.append(sco.linprog(c, A, b, method='revised simplex', options = {'maxiter': 1000,
                                                                                'tol':1e-19}))
    dT.append(time.process_time() - t0)
plt.plot(n, dT)
plt.show()

#def func(x):
#    return(2.718 ** x)
#
#popt, pcov = sco.curve_fit(func, n, dT)

