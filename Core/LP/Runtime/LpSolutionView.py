import tkinter as tk

import matplotlib
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Core.LP.Runtime.LpGraphBuilder import LpGraphBuilder
from Core.ScrollableFrame import ScrollableFrame

matplotlib.use('TkAgg')


class LpSolutionView(tk.Frame):
    def __init__(self, graph_builder: LpGraphBuilder, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)

        self.graph_builder = graph_builder
        self.scrollable_frame = ScrollableFrame(self)
        self.scrollable_frame.grid(column=0, row=0, sticky=tk.NSEW)
        self.scrollable_frame.get_container().columnconfigure(0, weight=1)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.canvases_datas = []

    def on_deselect(self):
        self.scrollable_frame.unfocus()
        self.__destroy_canvases()

    def on_select(self):
        self.scrollable_frame.focus()
        self.__create_canvases()

    def __create_canvases(self):
        plot = self.graph_builder.build_default_graph()
        if plot is not None:
            self.__create_canvas(plot)

        plots = self.graph_builder.build_patch_graphs()
        if plots is not None:
            for plot in plots:
                self.__create_canvas(plot)

        plot = self.graph_builder.build_result_graph()
        if plot is not None:
            self.__create_canvas(plot)

        plot = self.graph_builder.build_animated_result_graph()
        if plot is not None:
            self.__create_canvas(plot)

    def __create_canvas(self, plot):
        canvas = FigureCanvasTkAgg(plot[0], master=self.scrollable_frame.get_container())
        tk_canvas = canvas.get_tk_widget()
        tk_canvas.pack(side=tk.TOP, padx=10, pady=10)
        self.canvases_datas.append((canvas, plot))

    def __destroy_canvases(self):
        for canvas_data in self.canvases_datas:
            plt.close(canvas_data[1][0])
            tk_canvas = canvas_data[0].get_tk_widget()
            tk_canvas.grid_forget()
            tk_canvas.destroy()

        self.canvases_datas.clear()
