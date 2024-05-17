import tkinter as tk
from tkinter import ttk

from Core.LP.Runtime.LpModelView import LpModelView


class ModelsView(tk.Frame):
    current_view = None

    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)

        self.buttons_list = tk.Frame(self)
        self.buttons_list.pack(side=tk.LEFT, fill=tk.Y)

        separator = ttk.Separator(self, orient=tk.VERTICAL)
        separator.pack(side=tk.LEFT, fill=tk.Y)

        self.lp_button = tk.Button(self.buttons_list, text='ЛП', padx=20,
                                   command=self.select_lp_view)
        self.lp_button.pack(side=tk.TOP, padx=20, pady=20)

        self.overview = tk.Frame(self)
        self.overview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.lp_view = LpModelView(self.overview)

        overview_label_text = 'Для решения задачи:\n1. Выберите тип модели или метода.\n2. Введите условие задачи.\n'
        self.tutorial_label = tk.Label(self.overview, text=overview_label_text, justify=tk.LEFT)
        self.__show_tutorial_label()

    def focus(self):
        self.__deselect_lp()
        self.__show_tutorial_label()

    def unfocus(self):
        if self.current_view is None:
            return

    def __show_tutorial_label(self):
        self.tutorial_label.pack(fill=tk.BOTH, expand=True)

    def __hide_tutorial_label(self):
        self.tutorial_label.pack_forget()

    def select_lp_view(self):
        if self.current_view is self.lp_view:
            return

        self.__hide_tutorial_label()
        self.lp_view.pack(fill=tk.BOTH, expand=True)

        self.current_view = self.lp_view

    def __deselect_lp(self):
        if self.current_view is not self.lp_view:
            return

        self.lp_view.pack_forget()

    def get_lp_problem_view(self) -> LpModelView:
        return self.lp_view
