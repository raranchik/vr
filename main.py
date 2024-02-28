from data_list import *
from ortools_methods import *
from matplotlib_methods import *

data = create_data2()

status, x_values, optimum, solver = solve(data, 'clp')
print('Status code: %d\n' % status)
if status == pywraplp.Solver.OPTIMAL:
    print('\nSolution: OPTIMAL')
    print('Objective value =', optimum)
    k = 0
    for i in range(len(x_values)):
        for j in range(len(x_values[i])):
            print('x[%d] =' % k, x_values[i][j])
            k += 1
elif status == pywraplp.Solver.UNBOUNDED:
    print("The problem has no optimal solution due to unboundedness "
          "of the target function on the set of admissible solutions.")
elif status == pywraplp.Solver.INFEASIBLE:
    print("The problem has no solution due to inconsistency of constraints.")
else:
    print("The problem does not have an optimal solution.")

print('\nAdvanced usage:')
print('Problem solved in %f milliseconds' % solver.wall_time())
print('Problem solved in %d iterations' % solver.iterations())

draw2d(data, status, x_values, optimum, solver)
