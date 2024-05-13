import tkinter as tk
from tkinter import ttk
from Core.LP.Runtime.LpConstraintView import LpConstraintView


class LpConstraintsView(tk.Frame):
    constraints = []

    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)

        text = 'Добавить ограничение'
        add_constraint_button = tk.Button(self, text=text, command=self.add_constraint)
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

        frame = tk.Frame(self, bg='#de00da')
        frame.pack(fill=tk.BOTH, expand=True)
        canvas = tk.Canvas(frame, bg='#ff1500')
        scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview, bg='#00ff44')
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.constraints_frame = tk.Frame(canvas)

        def on_frame_configure(e):
            canvas.configure(scrollregion=canvas.bbox("all"))

        self.constraints_frame.bind("<Configure>", on_frame_configure)
        constraints_frame_id = canvas.create_window((0, 0), window=self.constraints_frame, anchor=tk.NW)
        canvas.configure(yscrollcommand=scrollbar.set)

        def on_mousewheel(e):
            canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", on_mousewheel)
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        def configure_frame(e):
            size = (self.constraints_frame.winfo_reqwidth(), self.constraints_frame.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if self.constraints_frame.winfo_reqwidth() != canvas.winfo_width():
                canvas.config(width=self.constraints_frame.winfo_reqwidth())

        self.constraints_frame.bind('<Configure>', configure_frame)

        def configure_canvas(e):
            if self.constraints_frame.winfo_reqwidth() != canvas.winfo_width():
                canvas.itemconfigure(constraints_frame_id, width=canvas.winfo_width())

        canvas.bind('<Configure>', configure_canvas)

    def hide(self):
        return

    def show(self):
        return

    def add_constraint(self):
        delete_cmnd = lambda cnstrnt: self.remove_constraint(cnstrnt)
        constraint = LpConstraintView(delete_cmnd, self.constraints_frame)
        constraint.pack(side=tk.TOP, expand=False)
        self.constraints.append(constraint)

    def remove_constraint(self, constraint):
        if constraint not in self.constraints:
            return

        constraint.pack_forget()
        constraint.destroy()

    def remove_constraints(self):
        for constraint in self.constraints:
            self.remove_constraint(constraint)

    def get_vars_constraints_sign(self):
        return self.vars_cnsts_sign

    def get_constraints(self):
        return self.constraints
