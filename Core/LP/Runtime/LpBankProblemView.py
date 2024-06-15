import os
import tkinter as tk

from PIL import ImageTk, Image

from Core.Helper.lp_bank import get_bank
from Core.LP.Runtime.LpProblemData import LpProblemData
from Core.ScrollableFrame import ScrollableFrame
from definitions import LP_ASSETS_PATH, resource_path


class LpBankView(tk.Frame):
    def __init__(self, args, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)

        self.scrollable_frame = ScrollableFrame(self)
        self.scrollable_frame.grid(column=0, row=0, sticky=tk.NSEW)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.bank = get_bank()
        self.previews = []

        container = self.scrollable_frame.get_container()
        for i in range(2):
            container.columnconfigure(i, weight=1)

        self.notebook = args[0]
        self.controller = args[1]
        self.view = args[2]

        n = len(self.bank)
        row_per_column = int(n / 2)
        column = 0
        row = 0
        for i in range(n):
            data = self.bank[str(i)]
            frame = tk.Frame(container)
            frame.grid(column=column, row=row, padx=20, pady=20, sticky=tk.NSEW)

            text = data['title']
            label = tk.Label(frame, text=text)
            label.pack(side=tk.TOP, pady=5)

            path = resource_path(os.path.join(LP_ASSETS_PATH, f'{i}_result_graph.png'))
            img = ImageTk.PhotoImage(Image.open(path))
            self.previews.append(img)
            label = tk.Label(frame, image=img)
            label.pack(side=tk.TOP, pady=5)

            text = 'Перейти к решению'
            button = tk.Button(frame, text=text, padx=20)
            button.configure(command=lambda key=str(i): self.select_problem(key))
            button.pack(side=tk.BOTTOM, pady=5)

            row += 1

            if row >= row_per_column:
                column += 1
                row = 0

    def select_problem(self, key):
        self.notebook.select(0)
        self.view.select_lp_view()
        data = self.bank[key]['data']
        problem = LpProblemData(data)
        self.controller.visualize_bank_problem(problem)
