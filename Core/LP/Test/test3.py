import tkinter as tk
from tkinter import ttk

# Создаем основное окно
root = tk.Tk()
root.title("Поиск экстремума функции")


# Функция для обновления текста в метке (если требуется)
def update_label(event):
    selected = combobox.get()
    # Здесь можно обновить метку или выполнить другие действия


# Создаем текстовое поле
text = tk.Text(root, height=1, width=40)
text.pack(padx=10, pady=10)

# Вставляем текст до Combobox
text.insert(tk.END, "Найти ")

# Создаем Combobox с вариантами min и max
combobox = ttk.Combobox(root, values=["min", "max"], state="readonly")
combobox.current(0)  # Устанавливаем начальное значение на "min"
combobox.bind("<<ComboboxSelected>>", update_label)

# Размещаем Combobox в текстовом поле
text.window_create(tk.END, window=combobox)

# Вставляем оставшуюся часть текста после Combobox
text.insert(tk.END, " значение функции:")

# Отключаем редактирование текстового поля
text.config(state=tk.DISABLED)

# Запуск основного цикла приложения
root.mainloop()
