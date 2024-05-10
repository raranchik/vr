from pyomo.environ import *

from definitions import IPOPT_PATH

# Создание модели
model = ConcreteModel()

# Определение переменной (без ограничений)
model.x = Var(within=Reals)


# Определение функции цели
def objective_rule(m):
    names = {'sin': sin, 'cos': cos, 'x': m.x}
    exp = 'sin(x) + x ** 2'
    f = eval(exp, names)
    return f


model.objective = Objective(rule=objective_rule, sense=minimize)

# Решение модели с использованием солвера Ipopt
solver = SolverFactory('ipopt', executable=IPOPT_PATH)
result = solver.solve(model, tee=True)  # tee=True для вывода процесса решения

# Вывод результата
x_optimal = model.x.value
print(f'Оптимальное значение x: {x_optimal:.4f}')
