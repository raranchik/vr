import tkinter as tk
from tkinter import ttk


class App1(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Задача линейного программирования")
        self.geometry("800x600")

        self.variables_count = 0
        self.objective_coeffs = []

        # Интерфейс для целевой функции
        self.obj_func_frame = tk.Frame(self)
        self.obj_func_frame.pack(fill=tk.X, pady=10)
        self.obj_func_label = tk.Label(self.obj_func_frame, text="Целевая функция:")
        self.obj_func_label.pack(side=tk.LEFT, padx=10)
        self.update_objective_function()

        # Кнопки для управления переменными
        self.variables_control_frame = tk.Frame(self)
        self.variables_control_frame.pack(fill=tk.X, pady=10)
        self.add_var_button = tk.Button(self.variables_control_frame, text="Добавить переменную",
                                        command=self.add_variable)
        self.add_var_button.pack(side=tk.LEFT, padx=5)
        self.remove_var_button = tk.Button(self.variables_control_frame, text="Удалить переменную",
                                           command=self.remove_variable)
        self.remove_var_button.pack(side=tk.LEFT, padx=5)

        # Создание области прокрутки для ограничений
        self.canvas = tk.Canvas(self)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Привязка события прокрутки к Canvas
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

        self.constraints_frame = tk.LabelFrame(self.scrollable_frame, text="Ограничения")
        self.constraints_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.add_constraint_button = tk.Button(self.scrollable_frame, text="Добавить ограничение",
                                               command=self.add_constraint)
        self.add_constraint_button.pack(pady=10)

        self.constraints = []

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def add_variable(self):
        self.variables_count += 1
        self.update_objective_function()
        self.update_constraints()

    def remove_variable(self):
        if self.variables_count > 0:
            self.variables_count -= 1
            self.objective_coeffs.pop()
            self.update_objective_function()
            self.update_constraints()

    def update_objective_function(self):
        for widget in self.obj_func_frame.winfo_children()[1:]:
            widget.destroy()
        for i in range(self.variables_count):
            coeff = tk.DoubleVar()
            entry = ttk.Entry(self.obj_func_frame, textvariable=coeff, width=5)
            entry.pack(side=tk.LEFT, padx=2)
            if len(self.objective_coeffs) < self.variables_count:
                self.objective_coeffs.append(coeff)
            else:
                entry.delete(0, tk.END)
                entry.insert(0, str(self.objective_coeffs[i].get()))

    def add_constraint(self):
        constraint = Constraint(self.variables_count, self.constraints_frame)
        self.constraints.append(constraint)
        constraint.frame.pack(fill=tk.X, pady=2)

    def update_constraints(self):
        for constraint in self.constraints:
            constraint.update(self.variables_count)

    def remove_constraint(self, constraint):
        constraint.frame.destroy()
        self.constraints.remove(constraint)


class Constraint:
    def __init__(self, var_count, master):
        self.frame = tk.Frame(master)
        self.entries = []
        self.inequality = tk.StringVar(value=">=")
        self.rhs = tk.DoubleVar()

        for _ in range(var_count):
            entry = tk.DoubleVar()
            entry_widget = ttk.Entry(self.frame, textvariable=entry, width=5)
            entry_widget.pack(side=tk.LEFT, padx=2)
            self.entries.append(entry)

        self.inequality_option = ttk.Combobox(self.frame, textvariable=self.inequality, values=[">=", "<=", "=="],
                                              width=3)
        self.inequality_option.pack(side=tk.LEFT, padx=2)

        rhs_entry = ttk.Entry(self.frame, textvariable=self.rhs, width=5)
        rhs_entry.pack(side=tk.LEFT, padx=2)

        delete_button = tk.Button(self.frame, text="Удалить",
                                  command=lambda: master.master.master.remove_constraint(self))
        delete_button.pack(side=tk.LEFT, padx=5)

    def update(self, var_count):
        current_count = len(self.entries)
        if var_count > current_count:
            for _ in range(var_count - current_count):
                entry = tk.DoubleVar()
                entry_widget = ttk.Entry(self.frame, textvariable=entry, width=5)
                entry_widget.pack(side=tk.LEFT, padx=2, before=self.inequality_option)
                self.entries.append(entry)
        elif var_count < current_count:
            for _ in range(current_count - var_count):
                entry_widget = self.entries.pop()
                entry_widget.pack_forget()


if __name__ == "__main__":
    app = App1()
    app.mainloop()
