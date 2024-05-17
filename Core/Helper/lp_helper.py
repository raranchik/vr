import numpy as np
from scipy.optimize import linprog


def solve_lp(problem):
    goal = problem.get_goal()
    c = np.array(problem.get_objv_c())
    A = []
    b = []

    for cons, sign in zip(problem.get_consrts_c(), problem.get_consrts_s()):
        if sign == '<=':
            A.append(cons[:-1])
            b.append(cons[-1])
        elif sign == '>=':
            A.append([-coeff for coeff in cons[:-1]])
            b.append(-cons[-1])

    A = np.array(A)
    b = np.array(b)

    bounds = []
    for var_cons, sign in zip(problem.get_var_consrts_c(), problem.get_var_consrts_s()):
        if sign == '>=':
            bounds.append((var_cons[0], None))
        elif sign == '<=':
            bounds.append((None, var_cons[0]))

    if goal == 'max':
        c = -c

    # Решение задачи линейного программирования
    result = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')

    return result
