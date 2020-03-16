import numpy as np
import matplotlib.pyplot as plt
import pulp

#Initialize variables
p1 = pulp.LpProblem("First_problem", pulp.LpMinimize)
#Initialize variables, Use LpContinuous for R, LpInteger
x1 = pulp.LpVariable("x1", 0, None, pulp.LpContinuous)
x2 = pulp.LpVariable("x2", 0, None, pulp.LpContinuous)
x3 = pulp.LpVariable("x3", 0, None, pulp.LpContinuous)
#Add the objective function
p1 += 2 * x1 + 7 * x2 + 2 * x3
#Add constraints
p1 += 1 * x1 + 4 * x2 + 1 * x3 >= 10.0, "First_constraint"
p1 += 4 * x1 + 2 * x2 + 2 * x3 >= 13, "Second_constraint"
p1 += 1 * x1 + 1 * x2 - 1 * x3 >= 0, "Third_constraint"
#Write LP into a .lp file
p1.writeLP("TP2LP2.lp")
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

#Integer part

#Initialize variables
p2 = pulp.LpProblem("First_problem", pulp.LpMinimize)
#Initialize variables, Use LpContinuous for R, LpInteger
x1 = pulp.LpVariable("x1", 0, None, pulp.LpInteger)
x2 = pulp.LpVariable("x2", 0, None, pulp.LpInteger)
x3 = pulp.LpVariable("x3", 0, None, pulp.LpInteger)
#Add the objective function
p2 += 2 * x1 + 7 * x2 + 2 * x3
#Add constraints
p2 += 1 * x1 + 4 * x2 + 1 * x3 >= 10.0, "First_constraint"
p2 += 4 * x1 + 2 * x2 + 2 * x3 >= 13, "Second_constraint"
p2 += 1 * x1 + 1 * x2 - 1 * x3 >= 0, "Third_constraint"
#Write LP into a .lp file
p2.writeLP("TP2LP2.lp")
#Solve the LP
#Another solver can be used by inserting it into the parenthesis ex : p1.solve(CPLEX())
p2.solve()
#Print status of the solution
print("Status:", pulp.LpStatus[p2.status])
#Print solution variables
for v in p2.variables():
    print(v.name, "=", v.varValue)
#Objective function value
print("Objective function value = ", pulp.value(p2.objective))