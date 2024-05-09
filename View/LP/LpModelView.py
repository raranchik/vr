import tkinter as tk

from View.LP.LpProblemView import LpProblemView
from View.LP.LpSolutionView import LpSolutionView


class LpModelView(tk.Frame):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)

        self.problem_view = LpProblemView(self, bg='#8b9428')
        self.problem_view.place(anchor=tk.NW, relwidth=.3, relheight=1.)

        self.solution_view = LpSolutionView(self, bg='#331869')
        self.solution_view.place(anchor=tk.NW, relx=.3, relwidth=.8, relheight=1.)

    def hide(self):
        self.problem_view.hide()
        self.solution_view.hide()

    def show(self):
        self.problem_view.show()
        self.solution_view.show()
