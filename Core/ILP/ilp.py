from pyomo.environ import *

from definitions import CBC_PATH

# Создаем модель
model = ConcreteModel()

# Объявляем переменные
model.x = Var(within=NonNegativeIntegers)
model.y = Var(within=NonNegativeIntegers)

# Целевая функция
model.objective = Objective(expr=3 * model.x + 2 * model.y, sense=minimize)

# Ограничения
model.constraint = Constraint(expr=model.x + model.y >= 1)

# Выбор солвера и решение
solver = SolverFactory('cbc', executable=CBC_PATH)
result = solver.solve(model)

# Выводим результат
print(f"Оптимальные значения: x = {value(model.x)}, y = {value(model.y)}")
print(f"Минимальное значение функции: {value(model.objective)}")
