import tkinter as tk
from tkinter import ttk

import matplotlib
import numpy as np
from matplotlib import pyplot as plt, animation
from matplotlib.animation import FuncAnimation
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from Core.Helper.lp_bank import problem1
from Core.Helper.lp_helper import solve_lp
from Core.Helper.lp_plot_helper import get_last_sequence_solution_plot_animated, get_sequence_solution_plot, \
    OPTIMAL_SOLUTION_COLOR, POINT_MARKER, LINES_LINESTYLE, LINES_WIDTH
from Core.LP.Runtime.LpProblemData import LpProblemData

matplotlib.use('TkAgg')


class LpSolutionsView(tk.Frame):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)

        # frame = tk.Frame(self, bg='#de00da')
        # frame.pack(fill=tk.BOTH, expand=True)
        # canvas = tk.Canvas(frame, bg='#ff1500')
        # scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview, bg='#00ff44')
        # scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=True)
        # canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # self.solutions_frame = tk.Frame(canvas)
        #
        # def on_frame_configure(e):
        #     canvas.configure(scrollregion=canvas.bbox("all"))
        #
        # self.solutions_frame.bind("<Configure>", on_frame_configure)
        # solutions_frame_id = canvas.create_window((0, 0), window=self.solutions_frame, anchor=tk.NW)
        # canvas.configure(yscrollcommand=scrollbar.set)
        #
        # def on_mousewheel(e):
        #     canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
        #
        # canvas.bind_all("<MouseWheel>", on_mousewheel)
        # canvas.xview_moveto(0)
        # canvas.yview_moveto(0)
        #
        # def configure_frame(e):
        #     size = (self.solutions_frame.winfo_reqwidth(), self.solutions_frame.winfo_reqheight())
        #     canvas.config(scrollregion="0 0 %s %s" % size)
        #     if self.solutions_frame.winfo_reqwidth() != canvas.winfo_width():
        #         canvas.config(width=self.solutions_frame.winfo_reqwidth())
        #
        # self.solutions_frame.bind('<Configure>', configure_frame)
        #
        # def configure_canvas(e):
        #     if self.solutions_frame.winfo_reqwidth() != canvas.winfo_width():
        #         canvas.itemconfigure(solutions_frame_id, width=canvas.winfo_width())
        #
        # canvas.bind('<Configure>', configure_canvas)

    def hide(self):
        return

    def show(self):
        return

    def add(self, plot):
        self.plot = plot
        canvas = FigureCanvasTkAgg(self.plot[0], master=self)
        canvas.get_tk_widget().grid(column=0, row=1)
