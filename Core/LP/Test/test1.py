from Core.Helper.lp_bank import get_bank
from Core.Helper.lp_helper import solve_lp
from Core.LP.Runtime.LpProblemData import LpProblemData

bank = get_bank()
for key, value in bank.items():
    print('##########################################################################')
    print(f'Problem {key}')
    problem = LpProblemData(value['data'])
    solve_result = solve_lp(problem)
    print(solve_result.status)
    if solve_result.status == 0:
        print('Optimization proceeding nominally.')
        optimal_value = solve_result.fun if problem.get_goal() == 'min' else -solve_result.fun
        print(f'Goal: {problem.get_goal()}')
        print(f'Optimal value: {optimal_value}')
        print(f'Optimal point: {solve_result.x}')
    elif solve_result.status == 1:
        print('Iteration limit reached.')
    elif solve_result.status == 2:
        print('Problem appears to be infeasible.')
    elif solve_result.status == 3:
        print('Problem appears to be unbounded.')
    elif solve_result.status == 4:
        print('Numerical difficulties encountered.')

    print(solve_result)
