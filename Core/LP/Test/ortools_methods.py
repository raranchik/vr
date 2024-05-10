import copy

from ortools.linear_solver import pywraplp


def solve(data, solver_id):
    solver = pywraplp.Solver.CreateSolver(solver_id)

    status, x_values, optimum, solver = solve_concrete_problem(data, solver)

    if status == pywraplp.Solver.OPTIMAL:
        inv_data = inverse_data(data)
        solver.Clear()
        inv_status, inv_x_values, inv_optimum, _ = solve_concrete_problem(inv_data, solver)
        if inv_status == pywraplp.Solver.OPTIMAL and optimum == inv_optimum and x_values != inv_x_values:
            x_values += inv_x_values

    return status, x_values, optimum, solver


def solve_concrete_problem(data, solver):
    num_vars = len(data['obj_coeffs'])
    x = {}
    for j in range(num_vars):
        x[j] = solver.NumVar(0, solver.infinity(), 'x[%i]' % j)

    num_constraints = len(data['constraint_coeffs'])
    for i in range(num_constraints):
        right = sum([x[j] * data['constraint_coeffs'][i][j] for j in range(num_vars)])
        left = data['bounds'][i]

        if data['signs'][i] == '<=':
            constraint = right <= left
        elif data['signs'][i] == '>=':
            constraint = right >= left
        elif data['signs'][i] == '=':
            constraint = right == left
        else:
            continue

        solver.Add(constraint)

    objective = sum([x[j] * data['obj_coeffs'][j] for j in range(num_vars)])
    if data['goal'] == 'max':
        solver.Maximize(objective)
    elif data['goal'] == 'min':
        solver.Minimize(objective)

    status = solver.Solve()

    x_values = []
    optimum = 0
    if status == pywraplp.Solver.OPTIMAL:
        value = [x[j].solution_value() for j in x]
        x_values.append(value)
        optimum = solver.Objective().Value()

    return status, x_values, optimum, solver


def inverse_data(data):
    inv_data = copy.deepcopy(data)

    inv_data['goal'] = 'max' if inv_data['goal'] == 'min' else 'min'

    num_constraints = len(inv_data['constraint_coeffs'])
    for i in range(num_constraints):
        if inv_data['signs'][i] == '<=':
            inv_data['signs'][i] = '>='
        elif inv_data['signs'][i] == '>=':
            inv_data['signs'][i] = '<='

    return inv_data
