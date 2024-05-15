from Core.Helper.lp_bank import *
from Core.Helper.lp_helper import solve_lp
from Core.LP.Runtime.LpModelView import LpModelView
from Core.LP.Runtime.LpProblemData import LpProblemData
from Core.LP.Runtime.LpSolutionGraphManager import LpSolutionGraphManager


class LpController:
    def __init__(self, model_view: LpModelView):
        self.model_view = model_view
        self.problem_view = self.model_view.get_problem_view()

        self.problem_view.add_solve_cmnd(self.visualize_solve_result)
        self.solutions_view = self.model_view.get_solution_view()
        self.solutions_view.on_tab_change_event.subscribe(self.__on_change_problem)

        self.problems = []

    def visualize_solve_result(self):
        # data = self.__read_input()
        # problem = LpProblemData(data)
        # if problem.is_invalid():
        #     return
        #
        # if self.__is_solved(problem):
        #     return

        problem = LpProblemData(problem1)
        self.problems.append(problem)
        solve_result = solve_lp(problem)
        visualize_manager = LpSolutionGraphManager(problem, solve_result, self)
        self.solutions_view.add_solution(visualize_manager)

    def objective_to_str(self, problem: LpProblemData):
        objv_c = problem.get_objv_c()
        objv_g = problem.get_goal()

        terms = [f"{coef}x_{i + 1}" for i, coef in enumerate(objv_c)]
        terms_str = " + ".join(terms)
        result = f"$F(x_1,x_2) = {terms_str} \\rightarrow {objv_g}$"

        return result

    def constraint_to_str(self, idx, problem: LpProblemData):
        consrt_c = problem.get_consrts_c()[idx]
        consrt_s = problem.get_consrts_s()[idx]

        terms = [f"{coef}x_{i + 1}" for i, coef in enumerate(consrt_c[:-1])]
        terms_str = " + ".join(terms)
        result = f"${terms_str} {consrt_s} {consrt_c[-1]}$"

        return result

    def var_constraints_to_str(self, problem: LpProblemData):
        var_consrts_s = problem.get_var_consrts_s()[0]

        n = 2
        variables = [f"x_{i + 1}" for i in range(n)]
        variables_str = ", ".join(variables)
        result = f"${variables_str} {var_consrts_s} 0$"

        return result

    def __read_input(self):
        objective, constraints = self.model_view.get_problem_input()
        data = {
            'objective': {},
            'constraints': {},
            'vars_constraints': {}
        }

        self.__read_objective(objective, data['objective'])
        self.__read_constraints(constraints[0], data['constraints'])
        self.__read_vars_constraints(constraints[1], data['vars_constraints'])

        return data

    def __read_objective(self, objective_input, container):
        container['goal'] = objective_input[0].get()
        coeffs_vars = objective_input[1]
        container['coefficients'] = (coeffs_vars[0].get(), coeffs_vars[1].get())

    def __read_constraints(self, constraints_input, container):
        container['coefficients'] = []
        container['signs'] = []
        for constraint in constraints_input:
            lhs = constraint.get_coeffs()
            rhs = constraint.get_bound()
            container['coefficients'].append((lhs[0].get(), lhs[1].get(), rhs.get()))

            sign = constraint.get_sign()
            container['signs'].append(sign.get())

    def __read_vars_constraints(self, constraints_input, container):
        sign = constraints_input.get()
        container['coefficients'] = [(.0, 1., .0), (1., .0, .0)]
        container['signs'] = [sign, sign]

    def __on_change_problem(self, idx):
        problem = self.problems[idx]
        self.problem_view.set_data(problem.data)

    def __is_solved(self, lhs):
        for rhs in self.problems:
            if lhs == rhs:
                return True

        return False
