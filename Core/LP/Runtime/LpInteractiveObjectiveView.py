import tkinter as tk
from tkinter import ttk
from Core.Helper.input_helper import on_validate_float
from Core.Event import Event as e_notifier


class LpInteractiveObjectiveView(tk.Frame):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)

        frame = tk.Frame(self)
        frame.pack(side=tk.TOP, anchor=tk.NW)

        text = 'Найти'
        label = tk.Label(frame, text=text, justify=tk.LEFT)
        label.pack(side=tk.LEFT)
        goals = ['min', 'max']
        self.goal_var = tk.StringVar(value='max')
        self.goal_var.trace_add('write', self.__on_modify_data)
        self.goal_combobox = ttk.Combobox(frame, textvariable=self.goal_var, values=goals, state='readonly', width=4,
                                          justify=tk.LEFT)
        self.goal_combobox.pack(side=tk.LEFT)

        text = 'значение функции:'
        label = tk.Label(frame, text=text, justify=tk.LEFT)
        label.pack(side=tk.LEFT)

        frame = tk.Frame(self)
        frame.pack(side=tk.TOP, anchor=tk.NW)

        text = 'F(x1, x2)='
        label = tk.Label(frame, text=text, justify=tk.LEFT)
        label.pack(side=tk.LEFT)

        n = 2
        self.x_vars = []
        for i in range(n):
            x_var = tk.StringVar(value='0.0')
            x_var.trace_add('write', self.__on_modify_data)
            x_spinbox = ttk.Spinbox(frame, textvariable=x_var, width=6, validate='key', justify=tk.RIGHT,
                                    increment=1., from_=-100, to=100)
            vcmd = (x_spinbox.register(on_validate_float), '%P')
            x_spinbox.config(validatecommand=vcmd)
            x_spinbox.pack(side=tk.LEFT)
            text = f'x{i + 1}'
            label = tk.Label(frame, text=text, justify=tk.LEFT)
            label.pack(side=tk.LEFT)
            self.x_vars.append(x_var)

            if i < n - 1:
                label = tk.Label(frame, text='+', justify=tk.LEFT)
                label.pack(side=tk.LEFT)

        text = 'при следующих ограничениях:'
        label = tk.Label(self, text=text, justify=tk.LEFT)
        label.pack(side=tk.TOP, anchor=tk.NW)

        self.modify_data_notifier = e_notifier()

    def get_coeffs(self):
        return self.x_vars

    def get_goal(self):
        return self.goal_var

    def set_data(self, data):
        objv_c = data['coefficients']
        for i, x_var in enumerate(self.x_vars):
            x_var.set(objv_c[i])

        objv_goal = data['goal']
        self.goal_var.set(objv_goal)

    def __on_modify_data(self, *args):
        self.modify_data_notifier.notify(*args)
