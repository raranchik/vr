import tkinter as tk
from Core.LP.Runtime.LpConstraintsView import LpConstraintsView
from Core.LP.Runtime.LpObjectiveView import LpObjectiveView


class LpProblemView(tk.Frame):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)

        self.objective_view = LpObjectiveView(self, bg='#8d22c7')
        self.objective_view.place(anchor=tk.NW, relwidth=1., relheight=0.2)

        self.constraints_view = LpConstraintsView(self, bg='#3d0a25')
        self.constraints_view.place(anchor=tk.NW, rely=.2, relwidth=1., relheight=.8)

        frame = tk.Frame(self, bg='#53997f')
        frame.pack(side=tk.BOTTOM, fill=tk.X)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        text = 'Решить'
        self.solve_button = tk.Button(frame, text=text)
        self.solve_button.grid(row=0, column=0)
        text = 'Очистить'
        clear_button = tk.Button(frame, text=text, command=self.constraints_view.remove_constraints)
        clear_button.grid(row=0, column=1)

    def hide(self):
        return

    def show(self):
        return

    def get_objective_input(self) -> tuple[tk.StringVar, list]:
        goal = self.objective_view.get_goal()
        coeffs = self.objective_view.get_coeffs()

        return goal, coeffs

    def get_constraints_input(self) -> tuple[list, tk.StringVar]:
        constraints = self.constraints_view.get_constraints()
        var_constraints = self.constraints_view.get_vars_constraints_sign()

        return constraints, var_constraints

    def add_solve_cmnd(self, cmnd):
        self.solve_button.configure(command=cmnd)
