import tkinter as tk

from tkinter import ttk

from Core.Event import Event
from Core.LP.Runtime.LpSolutionGraphManager import LpSolutionGraphManager
from Core.LP.Runtime.LpSolutionView import LpSolutionView


class LpSolutionsView(tk.Frame):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)

        self.notebook = ttk.Notebook(self, padding=0)
        self.notebook.grid(row=0, column=0, sticky=tk.NSEW)
        self.notebook.bind('<<NotebookTabChanged>>', self.__on_tab_change)
        self.columnconfigure(index=0, weight=1)
        self.rowconfigure(index=0, weight=1)

        self.selected_solution = -1
        self.solutions = []
        self.on_tab_change_event = Event()

    def add_solution(self, visualize_manager: LpSolutionGraphManager):
        self.__deselect_solution(self.selected_solution)

        frame = tk.Frame(self.notebook)
        solution = LpSolutionView(visualize_manager, master=frame)
        frame.pack(fill=tk.BOTH, expand=True)
        solution.pack(fill=tk.BOTH, expand=True)
        self.solutions.append(solution)

        idx = len(self.solutions) - 1
        self.notebook.add(frame, text=str(idx), padding=0, sticky=tk.NS + tk.EW, compound=tk.TOP)

        self.__select_solution(idx)
        self.notebook.select(idx)

    def __select_solution(self, idx: int):
        if idx == self.selected_solution:
            return

        if idx < 0 or idx >= len(self.solutions):
            return

        solution = self.solutions[idx]
        solution.on_select()
        solution.pack(fill=tk.BOTH, expand=True)

        self.selected_solution = idx

    def __deselect_solution(self, idx: int):
        if idx < 0 or idx >= len(self.solutions):
            return

        solution = self.solutions[idx]
        solution.on_deselect()
        solution.pack_forget()

    def __get_selected_tab_id(self) -> int:
        if self.notebook.select() == '':
            return -1

        return self.notebook.index(self.notebook.select())

    def __on_tab_change(self, e):
        if self.selected_solution < 0:
            return

        if self.selected_solution == self.__get_selected_tab_id():
            return

        self.__deselect_solution(self.selected_solution)
        self.__select_solution(self.__get_selected_tab_id())
        self.on_tab_change_event.notify(idx=self.selected_solution)
