import numpy as np
import matplotlib.pyplot as plt
import pulp
import csv

import csv

with open('DataElection.csv', newline='') as f:
    reader = csv.reader(f)
    pop = list(reader)
alpha = []
for i in range(52) :
    alpha.append("alpha" + str(i + 1))
print(alpha)
#Initialize variables
p1 = pulp.LpProblem("US Elections 2016", pulp.LpMinimize)
#Initialize variables, Use LpContinuous for R, LpInteger
u = pulp.LpVariable("u", 0, None, pulp.LpContinuous)
v = pulp.LpVariable("v", 0, None, pulp.LpContinuous)
for j in alpha :
    j = pulp.LpVariable(str(j), 0, None, pulp.LpInteger)
#Add the objective function
p1 += u - v
#Add constraints
p1 += 1 * x1 + 1 * x2 <= 6.0, "First constraint"
p1 += 9 * x1 + 5 * x2 <= 45.0, "Second constraint"
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