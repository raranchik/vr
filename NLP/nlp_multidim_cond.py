from pyomo.contrib.parmest.utils import ipopt_solve_with_stats
from pyomo.environ import *
from pyomo_helper import create_func_ref_dict
from definitions import IPOPT_PATH

# Создаем модель
model = ConcreteModel()

# Определяем переменные
model.x = Var(within=NonNegativeReals)
model.y = Var(within=NonNegativeReals)


# Целевая функция
def objective_rule(m):
    names = create_func_ref_dict()
    names['x'] = m.x
    names['y'] = m.y
    exp = 'pow(x,2)+pow(y,2)-x*y-10*x-4*y+60'
    f = eval(exp, names)

    return f


model.objective = Objective(rule=objective_rule, sense=minimize)

# Ограничения
model.constraint1 = Constraint(expr=model.x + 2 * model.y <= 20)
model.constraint2 = Constraint(expr=-model.x + 2 * model.y <= 30)

# Решаем модель
solver = SolverFactory('ipopt', executable=IPOPT_PATH)
results = solver.solve(model, tee=True)

# Выводим результат
x_opt = value(model.x)
y_opt = value(model.y)
objective_opt = value(model.objective)

print(f'Оптимальное значение x: {x_opt}')
print(f'Оптимальное значение y: {y_opt}')
print(f'Оптимальное значение целевой функции: {objective_opt}')
