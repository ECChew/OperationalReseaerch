import numpy as np
import scipy.optimize as sco
import matplotlib.pyplot as plt
import time
import statistics
from sklearn.linear_model import LinearRegression
import sklearn
import pandas as pd
from sklearn import metrics



#______Klee-Minty LP
n = [i for i in range(5, 21)]

res = []
dT = []

for i in n :
    A = np.zeros((i, i))
    b = []
    c = []
    tps = []
    for j in range(i):
        for k in range(i):
            if k == j :
                A[k, k] = 1
            else :
                A[j, k] = (2 * 10 ** (j - k))
        c.append(-10 ** (i - j))
        b.append(100 ** j)
    A = np.tril(A)
    for k in range(1) :
        t0 = time.time()
        res.append(sco.linprog(c, A, b, method='revised simplex', options = {'maxiter': 100000,
                                                                              'tol':1e-12}))
        tps.append(time.time() - t0)
    dT.append(statistics.mean(tps))


n = np.asarray([n]).reshape(-1, 1)
nL = np.asarray([np.log(n)]).reshape(-1, 1)
dTL = np.asarray([np.log(dT)]).reshape(-1, 1)
#Polynomial
regressorP = LinearRegression()
regressorP.fit(nL, dTL)
aP = np.exp(regressorP.intercept_)
bP = regressorP.coef_
yP = aP * np.power(n, bP)
#Exponential
regressorE = LinearRegression()
regressorE.fit(n, dTL)
aE = np.exp(regressorE.intercept_)
bE = regressorE.coef_
yE = aE * np.exp(bE * n)
# Find MSE
rE = metrics.r2_score(dT, yE)
rP = metrics.r2_score(dT, yP)

#Print results
print('Exponential : ')
print(r'$a_e$ = ', aE)
print(r'$b_e$ = ', bE)
print(r'$r^2(t=ae^{bx})$:',rE)
print('Polynomial : ')
print(r'$a_p$ = ', aP)
print(r'$b_p$ = ', bP)
print(r'$r^2(t=ax^b)$', rP)

ax = plt.axes()
plt.loglog(n, dT, label = 'true')
plt.loglog(n, yP, label = 'Polynomial')
plt.loglog(n, yE, label = 'Exponential')
#plt.loglog(n, (yP + yE) / 2, label = 'Mean')
plt.legend()
rexp = r'$r^2(t=ae^{bx}) =$' + str(rE)
rpol = r'$r^2(t=ax^b)=$' + str(rP)
ax.annotate(rexp, (10, 1e-2))
ax.annotate(rpol, (12, 1e-1))
plt.show()


ax = plt.axes()
plt.semilogy(n, dT, label = 'true')
plt.semilogy(n, yP, label = 'Polynomial')
plt.semilogy(n, yE, label = 'Exponential')
#plt.semilogy(n, (yP + yE) / 2, label = 'Mean')
ax.annotate(rexp, (10, 1e-2))
ax.annotate(rpol, (12, 1e-1))
plt.legend()
plt.show()