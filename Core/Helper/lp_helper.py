import numpy as np
from scipy.optimize import linprog

from Core.LP.Runtime.LpProblemData import LpProblemData


def solve_lp(problem: LpProblemData):
    goal = problem.get_goal()
    c = np.array(problem.get_objv_c())

    if goal == 'max':
        c = -c

    A = []
    b = []
    for coeffs in problem.get_consrts_c():
        A.append(coeffs[:-1])
        b.append(coeffs[-1])
    A = np.array(A)
    b = np.array(b)

    signs = problem.get_consrts_s()
    A_ub = A[[i for i in range(len(signs)) if signs[i] == '<=']]
    b_ub = b[[i for i in range(len(signs)) if signs[i] == '<=']]
    A_eq = A[[i for i in range(len(signs)) if signs[i] == '==']]
    b_eq = b[[i for i in range(len(signs)) if signs[i] == '==']]
    A_lb = A[[i for i in range(len(signs)) if signs[i] == '>=']]
    b_lb = b[[i for i in range(len(signs)) if signs[i] == '>=']]

    A_ub = np.vstack([A_ub, -A_lb])
    b_ub = np.concatenate([b_ub, -b_lb])

    var_coeffs = problem.get_var_consrts_c()
    var_signs = problem.get_var_consrts_s()
    for i, sign in enumerate(var_signs):
        if sign == '>=':
            A_ub = np.vstack([A_ub, -np.eye(len(var_coeffs))[i]])
            b_ub = np.concatenate([b_ub, [0]])
        elif sign == '<=':
            A_ub = np.vstack([A_ub, np.eye(len(var_coeffs))[i]])
            b_ub = np.concatenate([b_ub, [0]])

    result = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, method='highs')

    return result
