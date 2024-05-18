import tkinter as tk
from tkinter import ttk
from Core.LP.Runtime.LpInteractiveConstraintsView import LpInteractiveConstraintsView
from Core.LP.Runtime.LpInteractiveObjectiveView import LpInteractiveObjectiveView
from Core.Event import Event as e_notifier


class LpInteractiveProblemView(tk.Frame):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)

        self.objective = LpInteractiveObjectiveView(self)
        self.objective.modify_data_notifier.subscribe(self.__on_modify_data)
        self.objective.pack(side=tk.TOP, anchor=tk.NW)

        separator = ttk.Separator(self, orient=tk.HORIZONTAL)
        separator.pack(side=tk.TOP, fill=tk.X, pady=5)

        self.constraints = LpInteractiveConstraintsView(self)
        self.constraints.modify_data_notifier.subscribe(self.__on_modify_data)
        self.constraints.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        separator = ttk.Separator(self, orient=tk.HORIZONTAL)
        separator.pack(side=tk.TOP, fill=tk.X, pady=5)

        frame = tk.Frame(self)
        frame.pack(side=tk.BOTTOM)

        text = 'Очистить'
        clear_button = tk.Button(frame, text=text, command=self.constraints.remove_constraints, padx=20)
        clear_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.modify_data_notifier = e_notifier()

    def get_objective_input(self) -> tuple[tk.StringVar, list]:
        goal = self.objective.get_goal()
        coeffs = self.objective.get_coeffs()

        return goal, coeffs

    def get_constraints_input(self) -> tuple[list, tk.StringVar]:
        constraints = self.constraints.get_constraints()
        var_constraints = self.constraints.get_vars_constraints_sign()

        return constraints, var_constraints

    def set_data(self, data):
        self.objective.set_data(data['objective'])
        self.constraints.set_data(data['constraints'], data['vars_constraints'])

    def __on_modify_data(self, *args):
        self.modify_data_notifier.notify(*args)
