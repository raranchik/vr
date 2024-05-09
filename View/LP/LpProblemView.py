import tkinter as tk

from View.LP.LpConstraintsView import LpConstraintsView
from View.LP.LpObjectiveView import LpObjectiveView


class LpProblemView(tk.Frame):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)

        self.objective_view = LpObjectiveView(self, bg='#8d22c7')
        self.objective_view.place(anchor=tk.NW, relwidth=1., relheight=0.2)

        self.constraints_view = LpConstraintsView(self, bg='#3d0a25')
        self.constraints_view.place(anchor=tk.NW, rely=.2, relwidth=1., relheight=.8)

    def hide(self):
        return

    def show(self):
        return
