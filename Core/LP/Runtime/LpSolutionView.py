import tkinter as tk

import matplotlib
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Core.LP.Runtime.LpSolutionGraphManager import LpSolutionGraphManager
from Core.ScrollableFrame import ScrollableFrame

matplotlib.use('TkAgg')


class LpSolutionView(tk.Frame):
    def __init__(self, visualize_manager: LpSolutionGraphManager, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)

        self.visualize_manager = visualize_manager
        self.scrollable_frame = ScrollableFrame(self)
        self.scrollable_frame.pack(fill=tk.BOTH, expand=True)
        self.canvases_datas = []

    def on_deselect(self):
        self.scrollable_frame.unfocus()
        self.__destroy_canvases()

    def on_select(self):
        self.scrollable_frame.focus()
        self.__create_canvases()

    def __create_canvases(self):
        plot = self.visualize_manager.create_default_plot()
        self.__create_canvas(plot)

        for plot in self.visualize_manager.create_sequence_solution_plots():
            self.__create_canvas(plot)

        plot = self.visualize_manager.create_solution_result_plot()
        self.__create_canvas(plot)

    def __create_canvas(self, plot):
        canvas = FigureCanvasTkAgg(plot[0], master=self.scrollable_frame.get_container())
        tk_canvas = canvas.get_tk_widget()
        tk_canvas.pack(side=tk.TOP)

        self.canvases_datas.append((canvas, plot))

    def __destroy_canvases(self):
        for canvas_data in self.canvases_datas:
            plt.close(canvas_data[1][0])
            tk_canvas = canvas_data[0].get_tk_widget()
            tk_canvas.pack_forget()
            tk_canvas.destroy()

        self.canvases_datas.clear()
