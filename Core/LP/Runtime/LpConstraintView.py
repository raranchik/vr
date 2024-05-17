import tkinter as tk
from tkinter import ttk
from Core.Helper.input_helper import on_validate_float


class LpConstraintView(tk.Frame):
    def __init__(self, delete_cmnd, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)

        self.lhs: list[tk.DoubleVar] = []
        n = 2
        for cnstr_id in range(n):
            x_var = tk.DoubleVar(value=.0)
            x_entry = ttk.Entry(self, textvariable=x_var, width=6, validate='key', justify=tk.RIGHT)
            vcmd = (x_entry.register(on_validate_float), '%P')
            x_entry.config(validatecommand=vcmd)
            x_entry.pack(side=tk.LEFT)
            text = f'x{cnstr_id + 1}'
            label = tk.Label(self, text=text, justify=tk.LEFT)
            label.pack(side=tk.LEFT)
            self.lhs.append(x_var)

            if cnstr_id < n - 1:
                label = tk.Label(self, text='+', justify=tk.LEFT)
                label.pack(side=tk.LEFT)

        signs = ['>=', '<=', '==']
        self.sign = tk.StringVar(value=">=")
        self.signs_combobox = ttk.Combobox(self, textvariable=self.sign, values=signs,
                                           state='readonly', width=4, justify=tk.LEFT)
        self.signs_combobox.pack(side=tk.LEFT)

        self.rhs = tk.DoubleVar(value=.0)
        rhs_entry = ttk.Entry(self, textvariable=self.rhs, width=5)
        rhs_entry.pack(side=tk.LEFT)

        delete_button = tk.Button(self, text='Удалить', command=lambda: delete_cmnd(self))
        delete_button.pack(side=tk.LEFT)

    def get_coeffs(self):
        return self.lhs

    def get_sign(self):
        return self.sign

    def get_bound(self):
        return self.rhs

    def set_data(self, coeffs, sign):
        self.lhs[0].set(coeffs[0])
        self.lhs[1].set(coeffs[1])
        self.rhs.set(coeffs[2])
        self.sign.set(sign)

    def reset(self):
        for x_var in self.lhs:
            x_var.set(.0)

        self.rhs.set(.0)

        self.sign.set(">=")
