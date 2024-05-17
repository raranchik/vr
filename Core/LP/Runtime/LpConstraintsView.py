import tkinter as tk
from tkinter import ttk
from Core.LP.Runtime.LpConstraintView import LpConstraintView
from Core.Pool import Pool
from Core.ScrollableFrame import ScrollableFrame


class LpConstraintsView(tk.Frame):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)

        text = 'Добавить ограничение'
        add_constraint_button = tk.Button(self, text=text, command=self.__add_constraint, padx=20)
        add_constraint_button.pack(side=tk.TOP)

        frame = tk.Frame(self)
        frame.pack(side=tk.TOP)

        text = 'xi'
        label = tk.Label(frame, text=text, justify=tk.LEFT)
        label.pack(side=tk.LEFT)
        signs = ['>=', '<=']
        self.vars_cnsts_sign = tk.StringVar(value='>=')
        self.vars_cnsts_combobox = ttk.Combobox(frame, textvariable=self.vars_cnsts_sign, values=signs,
                                                state='readonly', width=4, justify=tk.LEFT)
        self.vars_cnsts_combobox.pack(side=tk.LEFT)

        text = '0'
        label = tk.Label(frame, text=text, justify=tk.LEFT)
        label.pack(side=tk.LEFT)

        separator = ttk.Separator(self, orient=tk.HORIZONTAL)
        separator.pack(side=tk.TOP, fill=tk.X, pady=5)

        self.scrollbar_frame = ScrollableFrame(self)
        self.scrollbar_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.constraints_pool = Pool(self.__create_constraint)
        self.constraints = []

    def remove_constraints(self):
        n = len(self.constraints)
        for _ in range(n):
            constraint = self.constraints[0]
            self.__remove_constraint(constraint)

    def get_vars_constraints_sign(self) -> tk.StringVar:
        return self.vars_cnsts_sign

    def get_constraints(self) -> list[LpConstraintView]:
        return self.constraints

    def set_data(self, consrts_data, var_consrts_data):
        consrts_c = consrts_data['coefficients']
        consrts_s = consrts_data['signs']

        n = len(consrts_c)
        for i, constraint in enumerate(self.constraints[n:]):
            self.__remove_constraint(constraint)

        n = n - len(self.constraints)
        for i in range(n):
            self.__add_constraint()

        for i, constraint in enumerate(self.constraints):
            constraint.set_data(consrts_c[i], consrts_s[i])

        var_consrts_s = var_consrts_data['signs']
        self.vars_cnsts_sign.set(var_consrts_s[0])

    def __add_constraint(self):
        constraint = self.constraints_pool.acquire()
        constraint.pack(side=tk.TOP, pady=5)
        self.constraints.append(constraint)

    def __remove_constraint(self, constraint):
        constraint.pack_forget()
        constraint.reset()
        self.constraints.remove(constraint)
        self.constraints_pool.release(constraint)

    def __create_constraint(self):
        constraint = LpConstraintView(self.__remove_constraint, self.scrollbar_frame.get_container())

        return constraint
