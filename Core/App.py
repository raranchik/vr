import tkinter as tk
from tkinter import ttk

from Core.BanksView import BanksView
from Core.LP.Runtime.LpController import LpController
from Core.ModelsView import ModelsView

MODELS_TAB_IDX = 0
BANKS_TAB_IDX = 1


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("VR")
        self.setup_window()

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill=tk.BOTH)

        self.models_view = ModelsView(self.notebook)
        self.models_view.pack(expand=True, fill=tk.BOTH)
        self.notebook.add(self.models_view, text='Модуль "Визуализация"')

        self.lp_controller = LpController(self.models_view.get_lp_problem_view())

        self.banks_view = BanksView(master=self.notebook, args=(self.notebook, self.lp_controller, self.models_view))
        self.banks_view.pack(expand=True, fill=tk.BOTH)
        self.notebook.add(self.banks_view, text='Модуль "Банк задач"')

    def setup_window(self):
        window_width = 1280
        window_height = 720

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
