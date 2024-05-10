import tkinter as tk
from tkinter import ttk
from Core.ModelsView import ModelsView


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("VR")
        self.setup_window()

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill=tk.BOTH)

        self.models_view = ModelsView(self)
        self.models_view.pack(expand=True, fill=tk.BOTH)
        self.notebook.add(self.models_view, text='Модели и методы')

        self.example_view = tk.Frame(self)
        self.example_view.pack(expand=True, fill=tk.BOTH)
        self.notebook.add(self.example_view, text='Примеры')

        self.theory_view = tk.Frame(self)
        self.theory_view.pack(expand=True, fill=tk.BOTH)
        self.notebook.add(self.theory_view, text='Теория')

        self.history_view = tk.Frame(self)
        self.history_view.pack(expand=True, fill=tk.BOTH)
        self.notebook.add(self.history_view, text='История')

        self.models_view.show()

    def setup_window(self):
        window_width = 1280
        window_height = 720

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
