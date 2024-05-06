import pyomo.environ as pyo
from pyomo.environ import *
from pyomo.opt import SolverFactory

# Create model
model = pyo.ConcreteModel()

# Create variables
model.x = pyo.Var(bounds=(0, 10))
model.y = pyo.Var(bounds=(0, 10))
x = model.x
y = model.y

# Constraints
model.C1 = pyo.Constraint(expr=-x+2*y<=8)
model.C2 = pyo.Constraint(expr=2*x+y<=14)
model.C3 = pyo.Constraint(expr=2*x-y<=10)

# Objective function
model.obj = pyo.Objective(expr=x+y, sense=maximize)

# Select solver
opt = SolverFactory('cbc', executable=r'C:/cbc/bin/cbc.exe')

# Solve optmization problem
opt.solve(model)

# Print model
model.pprint()

# Print x, y
x_value = pyo.value(x)
y_value = pyo.value(y)
print(f'x = {x_value}')
print(f'y = {y_value}')
