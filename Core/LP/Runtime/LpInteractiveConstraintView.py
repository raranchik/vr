import tkinter as tk
from tkinter import ttk
from Core.Helper.input_helper import on_validate_float
from Core.Event import Event as e_notifier


class LpInteractiveConstraintView(tk.Frame):
    def __init__(self, delete_cmnd, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)

        self.lhs = []
        self.lhs_traces = None
        n = 2
        for cnstr_id in range(n):
            x_var = tk.StringVar(value='0.0')
            x_spinbox = ttk.Spinbox(self, textvariable=x_var, width=6, validate='key', justify=tk.RIGHT,
                                    increment=1., from_=-100, to=100)
            vcmd = (x_spinbox.register(on_validate_float), '%P')
            x_spinbox.config(validatecommand=vcmd)
            x_spinbox.pack(side=tk.LEFT)
            text = f'x{cnstr_id + 1}'
            label = tk.Label(self, text=text, justify=tk.LEFT)
            label.pack(side=tk.LEFT)
            self.lhs.append(x_var)

            if cnstr_id < n - 1:
                label = tk.Label(self, text='+', justify=tk.LEFT)
                label.pack(side=tk.LEFT)

        signs = ['>=', '<=', '==']
        self.sign = tk.StringVar(value=">=")
        self.sign_trace = None
        self.signs_combobox = ttk.Combobox(self, textvariable=self.sign, values=signs,
                                           state='readonly', width=4, justify=tk.LEFT)
        self.signs_combobox.pack(side=tk.LEFT)

        self.rhs = tk.StringVar(value='0.0')
        self.rhs_trace = None
        rhs_spinbox = ttk.Spinbox(self, textvariable=self.rhs, width=6, validate='key', justify=tk.RIGHT,
                                  increment=1., from_=-100, to=100)
        rhs_spinbox.pack(side=tk.LEFT)

        def __delete_command():
            delete_cmnd(self)
            self.__on_modify_data()

        delete_button = tk.Button(self, text='Удалить', command=__delete_command)
        delete_button.pack(side=tk.LEFT)

        self.modify_data_notifier = e_notifier()

    def get_coeffs(self):
        return self.lhs

    def get_sign(self):
        return self.sign

    def get_bound(self):
        return self.rhs

    def set_data(self, coeffs, sign):
        self.lhs[0].set(coeffs[0])
        self.lhs[1].set(coeffs[1])
        self.rhs.set(coeffs[2])
        self.sign.set(sign)

    def reset(self):
        for x_var in self.lhs:
            x_var.set(.0)

        self.rhs.set(.0)

        self.sign.set(">=")

    def unbind_on_modify_data(self):
        if self.lhs_traces is not None:
            for i in range(len(self.lhs_traces)):
                trace = self.lhs_traces[i]
                self.lhs[i].trace_remove(trace[0], trace[1])

            self.lhs_traces = None

        if self.sign_trace is not None:
            self.sign.trace_remove(self.sign_trace[0], self.sign_trace[1])
            self.sign_trace = None

        if self.rhs_trace is not None:
            self.rhs.trace_remove(self.rhs_trace[0], self.rhs_trace[1])
            self.rhs_trace = None

    def bind_on_modify_data(self):
        mode = 'write'
        self.lhs_traces = []
        for i in range(len(self.lhs)):
            trace_name = self.lhs[i].trace_add(mode, self.__on_modify_data)
            self.lhs_traces.append((mode, trace_name))

        trace_name = self.sign.trace_add(mode, self.__on_modify_data)
        self.sign_trace = (mode, trace_name)

        trace_name = self.rhs.trace_add(mode, self.__on_modify_data)
        self.rhs_trace = (mode, trace_name)

    def __on_modify_data(self, *args):
        self.modify_data_notifier.notify(*args)
