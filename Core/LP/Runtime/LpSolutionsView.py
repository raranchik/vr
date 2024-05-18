import tkinter as tk
from Core.Event import Event
from Core.LP.Runtime.LpGraphBuilder import LpGraphBuilder
from Core.LP.Runtime.LpSolutionView import LpSolutionView
from Core.ScrollableNotebook import ScrollableNotebook


class LpSolutionsView(tk.Frame):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)

        self.notebook = ScrollableNotebook(self, enable_wheel_scroll=False, tab_menu=True)
        self.notebook.add_tab_changed_listener(self.__on_tab_change)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.selected_solution = -1
        self.solutions = []
        self.on_tab_change_event = Event()

    def add_solution(self, graph_builder):
        self.__deselect_solution(self.selected_solution)

        frame = tk.Frame(self.notebook)
        solution = LpSolutionView(graph_builder, master=frame)
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
        return self.notebook.get_selected_tab_id()

    def __on_tab_change(self, e):
        if self.selected_solution < 0:
            return

        if self.selected_solution == self.__get_selected_tab_id():
            return

        self.__deselect_solution(self.selected_solution)
        self.__select_solution(self.__get_selected_tab_id())
        self.on_tab_change_event.notify(idx=self.selected_solution)
