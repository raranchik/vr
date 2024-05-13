import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def plot():
    # Создание объекта Figure
    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)

    # Пример данных для графика
    x = [0, 1, 2, 3, 4]
    y = [0, 2, 4, 6, 8]

    # Построение графика
    ax.plot(x, y)
    ax.set_title("Пример графика")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")

    # Встраивание Figure в tkinter окно
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


# Создание окна tkinter
window = tk.Tk()
window.title("Пример отображения графика matplotlib в tkinter")

# Кнопка для построения графика
plot_button = ttk.Button(window, text="Построить график", command=plot)
plot_button.pack(side=tk.TOP)

# Запуск главного цикла
window.mainloop()
