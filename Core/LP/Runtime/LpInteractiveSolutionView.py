import tkinter as tk
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Core.ScrollableFrame import ScrollableFrame

matplotlib.use('TkAgg')


class LpInteractiveSolutionView(tk.Frame):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)

        self.scrollable_frame = ScrollableFrame(self)
        self.scrollable_frame.pack(fill=tk.BOTH, expand=True)
        self.scrollable_frame.get_container().columnconfigure(0, weight=1)

        self.canvases_datas = []
        self.last_graph_builder = None

    def on_deselect(self):
        self.scrollable_frame.unfocus()

    def on_select(self):
        self.scrollable_frame.focus()

    def add_solution(self, graph_builder):
        if self.last_graph_builder is not None:
            self.destroy_canvases()

        self.create_canvases(graph_builder)

    def create_canvases(self, graph_builder):
        plot = graph_builder.build_default_graph()
        if plot is not None:
            self.__create_canvas(plot)

        plots = graph_builder.build_patch_graphs()
        if plots is not None:
            for plot in plots:
                self.__create_canvas(plot)

        plot = graph_builder.build_result_graph()
        if plot is not None:
            self.__create_canvas(plot)

        plot = graph_builder.build_animated_result_graph()
        if plot is not None:
            self.__create_canvas(plot)

        self.last_graph_builder = graph_builder

    def __create_canvas(self, plot):
        canvas = FigureCanvasTkAgg(plot[0], master=self.scrollable_frame.get_container())
        tk_canvas = canvas.get_tk_widget()
        tk_canvas.pack(side=tk.TOP, padx=10, pady=10)
        self.canvases_datas.append((canvas, plot))

    def destroy_canvases(self):
        for canvas_data in self.canvases_datas:
            plot = canvas_data[1]
            self.last_graph_builder.release_graph(plot)

            tk_agg_canvas = canvas_data[0]
            tk_canvas = tk_agg_canvas.get_tk_widget()
            tk_canvas.grid_forget()
            tk_canvas.destroy()

        self.canvases_datas.clear()
