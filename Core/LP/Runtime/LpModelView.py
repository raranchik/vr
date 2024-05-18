import tkinter as tk
from tkinter import ttk
from Core.LP.Runtime.LpInteractiveProblemView import LpInteractiveProblemView
from Core.LP.Runtime.LpInteractiveSolutionView import LpInteractiveSolutionView
from Core.LP.Runtime.LpProblemView import LpProblemView
from Core.LP.Runtime.LpSolutionsView import LpSolutionsView
from Core.Event import Event as e_notifier


class LpModelView(tk.Frame):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)

        self.__init_simple_model()
        self.__init_interactive_model()

    def get_problem_input(self):
        objective = self.problem_view.get_objective_input()
        constraints = self.problem_view.get_constraints_input()

        return objective, constraints

    def get_interactive_problem_input(self):
        objective = self.interactive_problem_view.get_objective_input()
        constraints = self.interactive_problem_view.get_constraints_input()

        return objective, constraints

    def get_simple_problem_view(self):
        return self.problem_view

    def get_simple_solutions_view(self):
        return self.solutions_view

    def get_interactive_problem_view(self):
        return self.interactive_problem_view

    def get_interactive_solution_view(self):
        return self.interactive_solution_view

    def __open_simple_mode(self):
        self.interactive_model.pack_forget()
        self.simple_model.pack(fill=tk.BOTH, expand=True)

    def __open_interactive_mode(self):
        self.simple_model.pack_forget()
        self.interactive_model.pack(fill=tk.BOTH, expand=True)

    def __init_simple_model(self):
        self.simple_model = tk.Frame(self)
        self.simple_model.pack(fill=tk.BOTH, expand=True)

        frame = tk.Frame(self.simple_model)
        frame.pack(side=tk.LEFT, fill=tk.Y)

        self.problem_view = LpProblemView(frame)
        self.problem_view.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        text = 'Интерактивный\nрежим'
        self.interactive_button = tk.Button(frame, text=text, padx=20, command=self.__open_interactive_mode)
        self.interactive_button.pack(side=tk.BOTTOM, padx=10, pady=5)

        separator = ttk.Separator(frame, orient=tk.HORIZONTAL)
        separator.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

        self.solutions_view = LpSolutionsView(self.simple_model)
        self.solutions_view.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def __init_interactive_model(self):
        self.interactive_model = tk.Frame(self)

        frame = tk.Frame(self.interactive_model)
        frame.pack(side=tk.LEFT, fill=tk.Y)

        self.interactive_problem_view = LpInteractiveProblemView(frame)
        self.interactive_problem_view.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        text = 'Обычный\nрежим'
        self.simple_button = tk.Button(frame, text=text, padx=20, command=self.__open_simple_mode)
        self.simple_button.pack(side=tk.BOTTOM, padx=10, pady=5)

        separator = ttk.Separator(frame, orient=tk.HORIZONTAL)
        separator.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

        self.interactive_solution_view = LpInteractiveSolutionView(self.interactive_model)
        self.interactive_solution_view.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.modify_data_notifier = e_notifier()

        def on_modify_data(*args):
            self.modify_data_notifier.notify()

        self.interactive_problem_view.modify_data_notifier.subscribe(on_modify_data)
