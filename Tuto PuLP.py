import numpy as np
import matplotlib.pyplot as plt
import pulp

#Initialize variables
p1 = pulp.LpProblem("First problem", pulp.LpMinimize)
#Initialize variables, Use LpContinuous for R, LpInteger
x1 = pulp.LpVariable("x1", 0, None, pulp.LpContinuous)
x2 = pulp.LpVariable("x2", 0, None, pulp.LpContinuous)
#Add the objective function
p1 += -8 * x1 - 5 * x2
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