import math

from Core.Helper.lp_bank import get_bank
from Core.Helper.lp_helper import solve_lp
from Core.LP.Runtime.LpModelView import LpModelView
from Core.LP.Runtime.LpProblemData import LpProblemData
from Core.LP.Runtime.LpGraphBuilder import LpGraphBuilder


class LpController:
    def __init__(self, model_view: LpModelView):
        self.model_view = model_view
        self.problem_view = self.model_view.get_problem_view()

        self.problem_view.add_solve_cmnd(self.visualize_input_problem)
        self.solutions_view = self.model_view.get_solution_view()
        self.solutions_view.on_tab_change_event.subscribe(self.__on_change_problem)

        self.problems = []

    def visualize_input_problem(self):
        data = self.__read_input()
        problem = LpProblemData(data)
        if problem.is_invalid():
            return

        self.visualize_problem(problem)

    def visualize_bank_problem(self, problem):
        self.problem_view.set_data(problem.data)
        self.visualize_problem(problem)

    def visualize_problem(self, problem):
        if self.__is_solved(problem):
            return

        self.problems.append(problem)
        solve_result = solve_lp(problem)
        visualize_manager = LpGraphBuilder(problem, solve_result)  # , self)
        self.solutions_view.add_solution(visualize_manager)

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
