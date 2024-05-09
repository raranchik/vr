import tkinter as tk

from View.LP.LpModelView import LpModelView


class ModelsView(tk.Frame):
    active_view = None

    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)

        self.buttons_list = tk.Frame(self, bg='#FF5555')
        self.buttons_list.place(anchor=tk.NW, relwidth=.2, relheight=1.)

        self.overview = tk.Frame(self, bg='#CA6666')
        self.overview.place(anchor=tk.NW, relx=.2, relwidth=.8, relheight=1.)

        self.lp_button = tk.Button(self.buttons_list, text='ЛП')
        self.lp_button.pack(side=tk.TOP, fill=tk.X)
        self.lp_view = LpModelView(self.overview, bg='#8dc992')
        self.lp_button.configure(command=self.show_lp_view)

        self.nlp_button = tk.Button(self.buttons_list, text='НЛП')
        self.nlp_button.pack(side=tk.TOP, fill=tk.X)

        overview_label_text = 'Для решения задачи:\n1. Выберите тип модели или метода.\n2. Введите условие задачи.\n'
        self.overview_label = tk.Label(self.overview, text=overview_label_text, justify=tk.LEFT)

    def show(self):
        self.hide_lp_view()
        self.show_tutorial_label()

    def hide(self):
        if self.active_view is None:
            return

        self.active_view.hide()

    def show_tutorial_label(self):
        self.overview_label.place(anchor=tk.CENTER, relx=.5, rely=.5)

    def hide_tutorial_label(self):
        self.overview_label.place_forget()

    def show_lp_view(self):
        if self.active_view is self.lp_view:
            return

        self.hide_tutorial_label()
        self.lp_view.show()
        self.lp_view.pack(fill=tk.BOTH, expand=True)

        self.active_view = self.lp_view

    def hide_lp_view(self):
        if self.active_view is not self.lp_view:
            return

        self.lp_view.pack_forget()
        self.lp_view.hide()
