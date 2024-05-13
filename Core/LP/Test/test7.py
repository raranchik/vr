import tkinter as tk
from tkinter import Canvas
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np


class GraphApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Matplotlib and Tkinter Canvas with Pan and Zoom")

        # Создаем Canvas
        self.canvas_frame = tk.Frame(self)
        self.canvas_frame.pack(fill=tk.BOTH, expand=1)

        self.canvas = Canvas(self.canvas_frame, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        # Скроллбары для Canvas
        self.scroll_x = tk.Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.scroll_y = tk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        # Вставка matplotlib Figure в Canvas
        self.fig = Figure(figsize=(10, 6), dpi=100)
        self.axs = self.fig.subplots(2, 2)

        t = np.arange(0, 3, 0.01)

        # График 1
        self.axs[0, 0].plot(t, 2 * np.sin(2 * np.pi * t))
        self.axs[0, 0].set_title('Синус')

        # График 2
        self.axs[0, 1].plot(t, np.cos(2 * np.pi * t))
        self.axs[0, 1].set_title('Косинус')

        # График 3
        self.axs[1, 0].plot(t, np.tan(2 * np.pi * t))
        self.axs[1, 0].set_title('Тангенс')

        # График 4
        self.axs[1, 1].plot(t, np.exp(t))
        self.axs[1, 1].set_title('Экспонента')

        self.fig_canvas = FigureCanvasTkAgg(self.fig, master=self.canvas)
        self.fig_canvas.draw()

        self.fig_widget = self.fig_canvas.get_tk_widget()
        self.canvas.create_window((0, 0), window=self.fig_widget, anchor=tk.NW)

        # Привязка событий для панорамирования и масштабирования
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)

        self.scale_factor = 1.0

    def on_canvas_configure(self, event):
        # Обновляем область прокрутки
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_press(self, event):
        # Начало перемещения
        self.canvas.scan_mark(event.x, event.y)

    def on_drag(self, event):
        # Перемещение по Canvas
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def on_mousewheel(self, event):
        # Масштабирование Canvas
        scale_factor = 1.1 if event.delta > 0 else 0.9
        self.scale_factor *= scale_factor
        self.canvas.scale("all", event.x, event.y, scale_factor, scale_factor)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


if __name__ == "__main__":
    app = GraphApp()
    app.mainloop()
