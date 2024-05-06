import pyomo.environ as pyo
from pyomo.environ import *
from pyomo.opt import SolverFactory
import pandas as pd

# Inputs
data_gen = pd.DataFrame({
    'Cost': [.1, .05, .3, .4, .01],
    'Limit': [20, 10, 40, 50, 5]
})
data_load = pd.DataFrame({
    'Load_demand': [50, 20, 30]
})

n_generators = len(data_gen)  # number of generators

# Create model
model = pyo.ConcreteModel()
model.Pg = pyo.Var(range(n_generators), bounds=(0, None))
Pg = model.Pg

# Define Constraints
pg_sum = sum([Pg[g] for g in data_gen.index])
model.balance  = pyo.Constraint(expr= pg_sum == sum(data_load['Load_demand']))
model.cond = pyo.Constraint(expr= Pg[0] + Pg[3] >= data_load['Load_demand'][0])
model.limits = pyo.ConstraintList()
for g in data_gen.index:
    model.limits.add(expr=Pg[g]<=data_gen['Limit'][g])

model.pprint()

# Define object function
cost_sum = sum([Pg[g] * data_gen['Cost'][g] for g in data_gen.index])
model.obj = pyo.Objective(expr=cost_sum)

# Define solver
opt = SolverFactory('gurobi')

# Solve optimization problem
results = opt.solve(model)

# Add Pg column to data_gen DataFrame
data_gen['Power_generation'] = [pyo.value(Pg[g]) for g in data_gen.index]

# Sho DataFrame with Pg
print(data_gen)
