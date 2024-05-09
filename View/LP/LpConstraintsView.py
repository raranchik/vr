import tkinter as tk
from tkinter import ttk


class LpConstraintsView(tk.Frame):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)

        text = 'Добавить ограничение'
        add_constraint_button = tk.Button(self, text=text)
        add_constraint_button.pack(side=tk.TOP)

        frame = tk.Frame(self)
        frame.pack(side=tk.TOP)
        text = 'xi'
        label = tk.Label(frame, text=text, justify=tk.LEFT)
        label.pack(side=tk.LEFT, fill=tk.X)
        signs = ['>=', '<=']
        self.vars_constraints_sign = ttk.Combobox(frame, values=signs, state='readonly', width=4, justify=tk.LEFT)
        self.vars_constraints_sign.current(0)
        self.vars_constraints_sign.pack(side=tk.LEFT)
        text = '0'
        label = tk.Label(frame, text=text, justify=tk.LEFT)
        label.pack(side=tk.LEFT, fill=tk.X)

        frame = tk.Frame(self, bg='#7a4a10')
        frame.pack(fill=tk.BOTH, expand=True)

        frame = tk.Frame(self, bg='#53997f')
        frame.pack(side=tk.BOTTOM, fill=tk.X)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        text = 'Решить'
        solve_button = tk.Button(frame, text=text)
        solve_button.grid(row=0, column=0)
        text = 'Очистить'
        clear_button = tk.Button(frame, text=text)
        clear_button.grid(row=0, column=1)

    def hide(self):
        return

    def show(self):
        return

    def get_vars_constraints_sign(self):
        return self.vars_constraints_sign
