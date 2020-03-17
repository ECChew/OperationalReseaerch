import numpy as np
import matplotlib.pyplot as plt
import pulp
import csv

N = 538

with open('DataElection.csv', newline='') as f:
    reader = csv.reader(f)
    pop = list(reader)
alphalab = []
for i in range(len(pop)) :
    alphalab.append("alpha_" + str(i + 1))

#Initialize variables
p1 = pulp.LpProblem("US Elections 2016", pulp.LpMinimize)
#Initialize variables, Use LpContinuous for R, LpInteger
u = pulp.LpVariable("u", 0, None, pulp.LpContinuous)
v = pulp.LpVariable("v", 0, None, pulp.LpContinuous)
alpha = []
for j in alphalab :
    j = pulp.LpVariable(str(j), 0, None, pulp.LpInteger)
    alpha.append(j)
#Add the objective function
p1 += u - v
#Add constraints
for j in range(len(alphalab)) :
    p1 += v - alpha[j] * 1e6 / float(pop[j][0]) <= 0
    p1 += alpha[j] * 1e6 / float(pop[j][0]) - u <=0
#Add the last equality constraint
    p1 += sum(alpha) == N
#Write LP into a .lp file
p1.writeLP("TP2LP1.lp")
#Solve the LP
#Another solver can be used by inserting it into the parenthesis ex : p1.solve(CPLEX())
p1.solve()
#Print status of the solution
print("Status:", pulp.LpStatus[p1.status])
#Print solution variables
for v in p1.variables():
    print(v.name, "=", v.varValue)
#Objective function value
print("Objective function value = ", pulp.value(p1.objective))