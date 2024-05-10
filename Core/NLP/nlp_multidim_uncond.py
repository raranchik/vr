from pyomo.environ import *

from Core.Helper.pyomo_helper import create_func_ref_dict
from definitions import IPOPT_PATH

model = ConcreteModel()

model.x = Var(initialize=0.0, within=Reals)
model.y = Var(initialize=0.0, within=Reals)


def objective_function(m):
    names = create_func_ref_dict()
    names['x'] = m.x
    names['y'] = m.y
    exp = 'x ** 2 + y ** 2 - x * y + 3 * x - 4 * y'
    f = eval(exp, names)
    return f


model.objective = Objective(rule=objective_function, sense=minimize)

solver = SolverFactory('ipopt', executable=IPOPT_PATH)
solver.solve(model)

x_value = model.x.value
y_value = model.y.value
objective_value = model.objective()

print(f"Оптимальное значение x: {x_value}")
print(f"Оптимальное значение y: {y_value}")
print(f"Значение целевой функции в оптимальной точке: {objective_value}")
