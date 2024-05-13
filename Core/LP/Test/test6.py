# import tkinter as tk
# from tkinter import ttk
# from matplotlib.figure import Figure
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# import numpy as np
#
#
# class ZoomPanCanvas(tk.Canvas):
#     def __init__(self, parent, **kwargs):
#         super().__init__(parent, **kwargs)
#         self.bind("<ButtonPress-1>", self.on_button_press)
#         self.bind("<B1-Motion>", self.on_move_press)
#         self.bind("<MouseWheel>", self.on_mouse_wheel)
#
#         self.scale = 1.0
#         self.offset_x = 0
#         self.offset_y = 0
#         self.img = None
#
#     def load_graphs(self, fig):
#         self.fig = fig
#         self.draw_figure()
#
#     def draw_figure(self):
#         self.delete("all")
#         self.fig.canvas.draw()
#         width, height = self.fig.get_size_inches() * self.fig.get_dpi()
#         self.img = tk.PhotoImage(master=self, width=int(width), height=int(height))
#         self.create_image(self.offset_x, self.offset_y, image=self.img, anchor="nw")
#
#     def on_button_press(self, event):
#         self.scan_mark(event.x, event.y)
#
#     def on_move_press(self, event):
#         self.scan_dragto(event.x, event.y, gain=1)
#         self.offset_x -= (event.x - event.x_root)
#         self.offset_y -= (event.y - event.y_root)
#
#     def on_mouse_wheel(self, event):
#         scale = 1.0
#         if event.delta > 0:
#             scale *= 1.1
#         elif event.delta < 0:
#             scale /= 1.1
#         self.scale *= scale
#         self.scale_canvas(scale, event.x, event.y)
#
#     def scale_canvas(self, scale, x, y):
#         # self.scale(scale, scale, x, y)
#         self.configure(scrollregion=self.bbox("all"))
#         self.draw_figure()
#
#
# def plot_graphs():
#     fig = Figure(figsize=(10, 8), dpi=100)
#
#     ax1 = fig.add_subplot(221)
#     ax2 = fig.add_subplot(222)
#     ax3 = fig.add_subplot(223)
#     ax4 = fig.add_subplot(224)
#
#     x = np.linspace(0, 10, 100)
#     y1 = np.sin(x)
#     y2 = np.cos(x)
#     y3 = np.tan(x)
#     y4 = np.exp(-x)
#
#     ax1.plot(x, y1, label='sin(x)')
#     ax2.plot(x, y2, label='cos(x)')
#     ax3.plot(x, y3, label='tan(x)')
#     ax4.plot(x, y4, label='exp(-x)')
#
#     ax1.set_title("График 1")
#     ax2.set_title("График 2")
#     ax3.set_title("График 3")
#     ax4.set_title("График 4")
#
#     for ax in fig.get_axes():
#         ax.legend()
#
#     return fig
#
#
# def main():
#     root = tk.Tk()
#     root.title("Zoom and Pan Canvas")
#
#     zoom_pan_canvas = ZoomPanCanvas(root, width=800, height=600)
#     zoom_pan_canvas.pack(fill=tk.BOTH, expand=True)
#
#     fig = plot_graphs()
#     zoom_pan_canvas.load_graphs(fig)
#
#     root.mainloop()
#
#
# if __name__ == "__main__":
#     main()