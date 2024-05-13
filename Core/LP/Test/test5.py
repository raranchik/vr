import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


def plot():
    # Создание объекта Figure
    fig = Figure(figsize=(10, 8), dpi=100)

    # Создание нескольких графиков (2x2)
    ax1 = fig.add_subplot(221)
    ax2 = fig.add_subplot(222)
    ax3 = fig.add_subplot(223)
    ax4 = fig.add_subplot(224)

    # Пример данных для графиков
    x = [0, 1, 2, 3, 4]
    y1 = [0, 2, 4, 6, 8]
    y2 = [0, 1, 4, 9, 16]
    y3 = [0, 3, 6, 9, 12]
    y4 = [0, 4, 8, 12, 16]

    # Построение графиков
    ax1.plot(x, y1, label='y = 2x')
    ax2.plot(x, y2, label='y = x^2')
    ax3.plot(x, y3, label='y = 3x')
    ax4.plot(x, y4, label='y = 4x')

    # Настройка заголовков и легенд
    ax1.set_title("График 1")
    ax2.set_title("График 2")
    ax3.set_title("График 3")
    ax4.set_title("График 4")

    ax1.legend()
    ax2.legend()
    ax3.legend()
    ax4.legend()

    # Встраивание Figure в tkinter окно
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    tk_canvas = canvas.get_tk_widget()
    tk_canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # Добавление панели инструментов для навигации
    toolbar = NavigationToolbar2Tk(canvas, window)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    scale_f = 1.0

    def on_button_press(e):
        tk_canvas.scan_mark(e.x, e.y)
        pass

    def on_move_press(e):
        tk_canvas.scan_dragto(e.x, e.y, gain=1)
        pass

    def on_mouse_wheel(e):
        scale = 1.0
        if e.delta > 0:
            scale *= 1.1
        elif e.delta < 0:
            scale /= 1.1

        scale_f *= scale
        tk_canvas.scale('all', e.x, e.y, scale, scale)
        tk_canvas.configure(scrollregion=tk_canvas.bbox('all'))
        canvas.draw()
        pass

    tk_canvas.bind("<ButtonPress-1>", on_button_press)
    tk_canvas.bind("<B1-Motion>", on_move_press)
    tk_canvas.bind("<MouseWheel>", on_mouse_wheel)


# Создание окна tkinter
window = tk.Tk()
window.title("Сравнение нескольких графиков в tkinter")

# Кнопка для построения графиков
plot_button = ttk.Button(window, text="Построить графики", command=plot)
plot_button.pack(side=tk.TOP)

# Запуск главного цикла
window.mainloop()
