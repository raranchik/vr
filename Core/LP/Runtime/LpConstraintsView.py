import tkinter as tk
from tkinter import ttk
from Core.LP.Runtime.LpConstraintView import LpConstraintView
from Core.Pool import Pool


class LpConstraintsView(tk.Frame):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)

        text = 'Добавить ограничение'
        add_constraint_button = tk.Button(self, text=text, command=self.__add_constraint)
        add_constraint_button.pack(side=tk.TOP)

        frame = tk.Frame(self)
        frame.pack(side=tk.TOP)
        text = 'xi'
        label = tk.Label(frame, text=text, justify=tk.LEFT)
        label.pack(side=tk.LEFT, fill=tk.X)
        signs = ['>=', '<=']
        self.vars_cnsts_sign = tk.StringVar(value='>=')
        self.vars_cnsts_combobox = ttk.Combobox(frame, textvariable=self.vars_cnsts_sign, values=signs,
                                                state='readonly', width=4, justify=tk.LEFT)
        self.vars_cnsts_combobox.pack(side=tk.LEFT)
        text = '0'
        label = tk.Label(frame, text=text, justify=tk.LEFT)
        label.pack(side=tk.LEFT, fill=tk.X)

        self.constraints: list[LpConstraintView] = []

        frame = tk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True)
        canvas = tk.Canvas(frame)
        scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.constraints_frame = tk.Frame(canvas)

        def __on_frame_configure(e):
            canvas.configure(scrollregion=canvas.bbox("all"))

        self.constraints_frame.bind("<Configure>", __on_frame_configure)
        canvas.create_window((0, 0), window=self.constraints_frame, anchor=tk.NW)
        canvas.configure(yscrollcommand=scrollbar.set)

        def __on_mousewheel(e):
            canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", __on_mousewheel)
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        def __configure_frame(e):
            size = (self.constraints_frame.winfo_reqwidth(), self.constraints_frame.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if self.constraints_frame.winfo_reqwidth() != canvas.winfo_width():
                canvas.config(width=self.constraints_frame.winfo_reqwidth())

        self.constraints_frame.bind('<Configure>', __configure_frame)

        self.constraints_pool = Pool(self.__create_constraint)

    def remove_constraints(self):
        for constraint in self.constraints:
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
        constraint.pack(side=tk.TOP, expand=False)
        self.constraints.append(constraint)

    def __remove_constraint(self, constraint):
        constraint.pack_forget()
        self.constraints.remove(constraint)
        self.constraints_pool.release(constraint)

    def __create_constraint(self):
        constraint = LpConstraintView(self.__remove_constraint, self.constraints_frame)

        return constraint
