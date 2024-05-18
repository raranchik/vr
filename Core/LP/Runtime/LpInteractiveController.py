from matplotlib import pyplot as plt

from Core.Helper.input_helper import floatize
from Core.Helper.lp_helper import *
from Core.LP.Runtime.LpProblemData import LpProblemData
from Core.LP.Runtime.LpGraphBuilder import LpGraphBuilder
from Core.Pool import Pool


class LpInteractiveController:
    def __init__(self, model_view):
        self.model_view = model_view
        self.problem_view = self.model_view.get_interactive_problem_view()
        self.solution_view = self.model_view.get_interactive_solution_view()

        self.problem_view.modify_data_notifier.subscribe(self.visualize_input_problem)

        def create_plot_instance():
            return plt.subplots()

        self.plot_pool = Pool(create_plot_instance)

    def visualize_input_problem(self, *args):
        data = self.__read_input()
        problem = LpProblemData(data)
        if problem.is_invalid():
            return

        self.visualize_problem(problem)

    def visualize_problem(self, problem):
        solve_result = solve_lp(problem)
        visualize_manager = LpGraphBuilder(problem, solve_result, self.plot_pool)
        self.solution_view.add_solution(visualize_manager)

        print(solve_result)

    def __read_input(self):
        objective, constraints = self.model_view.get_interactive_problem_input()
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
        container['coefficients'] = (floatize(coeffs_vars[0].get()), floatize(coeffs_vars[1].get()))

    def __read_constraints(self, constraints_input, container):
        container['coefficients'] = []
        container['signs'] = []
        for constraint in constraints_input:
            lhs = constraint.get_coeffs()
            rhs = constraint.get_bound()
            container['coefficients'].append((floatize(lhs[0].get()), floatize(lhs[1].get()), floatize(rhs.get())))

            sign = constraint.get_sign()
            container['signs'].append(sign.get())

    def __read_vars_constraints(self, constraints_input, container):
        sign = constraints_input.get()
        container['coefficients'] = [(.0, 1., .0), (1., .0, .0)]
        container['signs'] = [sign, sign]
