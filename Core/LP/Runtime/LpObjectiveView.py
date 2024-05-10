import tkinter as tk
from tkinter import ttk
from Core.Helper.input_helper import on_validate_float


class LpObjectiveView(tk.Frame):
    x_coeffs = []

    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)

        sticky = tk.W
        for c in range(3):
            self.rowconfigure(index=c, weight=1)

        frame = tk.Frame(self, bg='#7a102c')
        frame.grid(row=0, sticky=sticky)
        text = 'Найти'
        label = tk.Label(frame, text=text, justify=tk.LEFT)
        label.pack(side=tk.LEFT)
        goals = ['min', 'max']
        self.goal = tk.StringVar(value='min')
        self.goal_combobox = ttk.Combobox(frame, textvariable=self.goal, values=goals, state='readonly', width=4,
                                          justify=tk.LEFT)
        self.goal_combobox.pack(side=tk.LEFT)
        text = 'значение функции:'
        label = tk.Label(frame, text=text, justify=tk.LEFT)
        label.pack(side=tk.LEFT)

        frame = tk.Frame(self)
        frame.grid(row=1, sticky=sticky)
        text = 'F(x1, x2)='
        label = tk.Label(frame, text=text, justify=tk.LEFT)
        label.pack(side=tk.LEFT)
        n = 2
        for i in range(n):
            x_coef = tk.DoubleVar(value=.0)
            x_entry = ttk.Entry(frame, textvariable=x_coef, width=6, validate='key', justify=tk.RIGHT)
            vcmd = (x_entry.register(on_validate_float), '%P')
            x_entry.config(validatecommand=vcmd)
            x_entry.pack(side=tk.LEFT)
            text = f'x{i + 1}'
            label = tk.Label(frame, text=text, justify=tk.LEFT)
            label.pack(side=tk.LEFT)
            self.x_coeffs.append(x_coef)

            if i < n - 1:
                label = tk.Label(frame, text='+', justify=tk.LEFT)
                label.pack(side=tk.LEFT)

        text = 'при следующих ограничениях:'
        label = tk.Label(self, text=text, justify=tk.LEFT)
        label.grid(row=2, sticky=sticky)

    def hide(self):
        return

    def show(self):
        return

    def get_coeffs(self):
        return self.x_coeffs

    def get_objective_goal(self):
        return self.goal