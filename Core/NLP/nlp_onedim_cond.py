from pyomo.environ import *

from Core.Helper.pyomo_helper import create_func_ref_dict
from definitions import IPOPT_PATH

# Создаем модель
model = ConcreteModel()

# Определяем переменную x
model.x = Var(domain=Reals)


def objective_rule(m):
    names = create_func_ref_dict()
    names['x'] = m.x
    exp = 'exp(x) - 4 * x'
    f = eval(exp, names)
    return f


# Определяем целевую функцию
model.objective = Objective(expr=objective_rule, sense=minimize)

# Добавляем ограничения
model.constraint1 = Constraint(expr=model.x >= 1)  # Линейное ограничение
model.constraint3 = Constraint(expr=model.x <= 4)  # Ограничение неравенства

# Выбираем солвер
solver = SolverFactory('ipopt', executable=IPOPT_PATH)

# Решаем задачу
solver.solve(model)

# Выводим результаты
x_value = value(model.x)
objective_value = value(model.objective)

print(f"Оптимальное значение x: {x_value}")
print(f"Значение целевой функции: {objective_value}")
