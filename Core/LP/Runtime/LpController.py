import math

from Core.Helper.lp_bank import problem1
from Core.Helper.lp_helper import solve_lp
from Core.Helper.lp_plot_helper import get_sequence_solution_plots, get_last_sequence_solution_plot_animated
from Core.LP.Runtime import LpModelView
from Core.LP.Runtime.LpProblemData import LpProblemData

ABS_TOL = 1e-10


class LpController:
    def __init__(self, model_view: LpModelView):
        self.model_view = model_view
        self.problem_view = self.model_view.get_problem_view()

        self.problem_view.add_solve_cmnd(self.solve_problem)
        self.solutions_view = model_view.get_solution_view()

    def solve_problem(self):
        # problem = self.read_input()
        # if not self.validate_input(problem):
        #     return

        # plots = get_sequence_solution_plots(problem)
        problem = LpProblemData(problem1)
        solve_result = solve_lp(problem)
        last_plot = get_last_sequence_solution_plot_animated(problem, solve_result)

        # n = len(plots)
        # for i in range(n):
        #     fig, ax = plots[i]
        #     self.solutions_view.add(fig)

        self.solutions_view.add(last_plot)
        # self.solutions_view.add(None)

    def read_input(self) -> LpProblemData:
        objective, constraints = self.model_view.get_problem_input()
        data = {
            'objective': {},
            'constraints': {},
            'vars_constraints': {}
        }

        self.read_objective(objective, data['objective'])
        self.read_constraints(constraints[0], data['constraints'])
        self.read_vars_constraints(constraints[1], data['vars_constraints'])

        return LpProblemData(data)

    def validate_input(self, problem: LpProblemData):
        objv_c = problem.get_objv_c()
        if math.isclose(objv_c[0], .0, abs_tol=ABS_TOL) and math.isclose(objv_c[1], .0, abs_tol=ABS_TOL):
            return False

        consrts_c = problem.get_consrts_c()
        if len(consrts_c) == 0:
            return False

        for i, (a0, b0, c0) in enumerate(consrts_c):
            if (math.isclose(a0, .0, abs_tol=ABS_TOL)
                    and math.isclose(b0, .0, abs_tol=ABS_TOL)
                    and math.isclose(c0, .0, abs_tol=ABS_TOL)):
                return False

        return True

    def read_objective(self, objective_input, container):
        container['goal'] = objective_input[0].get()
        coeffs_vars = objective_input[1]
        container['coefficients'] = (coeffs_vars[0].get(), coeffs_vars[1].get())

    def read_constraints(self, constraints_input, container):
        container['coefficients'] = []
        container['signs'] = []
        for constraint in constraints_input:
            lhs = constraint.get_coeffs()
            rhs = constraint.get_bound()
            container['coefficients'].append((lhs[0].get(), lhs[1].get(), rhs.get()))

            sign = constraint.get_sign()
            container['signs'].append(sign.get())

    def read_vars_constraints(self, constraints_input, container):
        sign = constraints_input.get()
        container['coefficients'] = [(.0, 1., .0), (1., .0, .0)]
        container['signs'] = [sign, sign]
