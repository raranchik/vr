import tkinter as tk
from tkinter import ttk

from Core.LP.Runtime.LpConstraintsView import LpConstraintsView
from Core.LP.Runtime.LpObjectiveView import LpObjectiveView


class LpProblemView(tk.Frame):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)

        self.objective = LpObjectiveView(self)
        self.objective.pack(side=tk.TOP, anchor=tk.NW)

        separator = ttk.Separator(self, orient=tk.HORIZONTAL)
        separator.pack(side=tk.TOP, fill=tk.X, pady=5)

        self.constraints = LpConstraintsView(self)
        self.constraints.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        separator = ttk.Separator(self, orient=tk.HORIZONTAL)
        separator.pack(side=tk.TOP, fill=tk.X, pady=5)

        frame = tk.Frame(self)
        frame.pack(side=tk.BOTTOM)

        text = 'Решить'
        self.solve_button = tk.Button(frame, text=text, padx=20)
        self.solve_button.pack(side=tk.LEFT, padx=10, pady=5)

        text = 'Очистить'
        clear_button = tk.Button(frame, text=text, command=self.constraints.remove_constraints, padx=20)
        clear_button.pack(side=tk.LEFT, padx=10, pady=5)

    def get_objective_input(self) -> tuple[tk.StringVar, list]:
        goal = self.objective.get_goal()
        coeffs = self.objective.get_coeffs()

        return goal, coeffs

    def get_constraints_input(self) -> tuple[list, tk.StringVar]:
        constraints = self.constraints.get_constraints()
        var_constraints = self.constraints.get_vars_constraints_sign()

        return constraints, var_constraints

    def add_solve_cmnd(self, cmnd):
        self.solve_button.configure(command=cmnd)

    def set_data(self, data):
        self.objective.set_data(data['objective'])
        self.constraints.set_data(data['constraints'], data['vars_constraints'])
