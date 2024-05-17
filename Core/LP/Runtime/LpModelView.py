import tkinter as tk
from Core.LP.Runtime.LpProblemView import LpProblemView
from Core.LP.Runtime.LpSolutionsView import LpSolutionsView


class LpModelView(tk.Frame):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)

        self.problem_view = LpProblemView(self)
        self.problem_view.pack(side=tk.LEFT, fill=tk.Y)

        self.solution_view = LpSolutionsView(self)
        self.solution_view.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def get_problem_input(self):
        objective = self.problem_view.get_objective_input()
        constraints = self.problem_view.get_constraints_input()

        return objective, constraints

    def get_problem_view(self) -> LpProblemView:
        return self.problem_view

    def get_solution_view(self) -> LpSolutionsView:
        return self.solution_view
