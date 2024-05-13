import tkinter as tk
from Core.LP.Runtime.LpProblemView import LpProblemView
from Core.LP.Runtime.LpSolutionsView import LpSolutionsView


class LpModelView(tk.Frame):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)

        self.problem_view = LpProblemView(self, bg='#8b9428')
        self.problem_view.place(anchor=tk.NW, relwidth=.3, relheight=1.)

        self.solution_view = LpSolutionsView(self, bg='#fc4c00')
        self.solution_view.place(anchor=tk.NW, relx=.3, relwidth=.8, relheight=1.)

    def hide(self):
        self.problem_view.hide()
        self.solution_view.hide()

    def show(self):
        self.problem_view.show()
        self.solution_view.show()

    def get_problem_input(self):
        objective = self.problem_view.get_objective_input()
        constraints = self.problem_view.get_constraints_input()

        return objective, constraints

    def get_problem_view(self) -> LpProblemView:
        return self.problem_view

    def get_solution_view(self) -> LpSolutionsView:
        return self.solution_view
