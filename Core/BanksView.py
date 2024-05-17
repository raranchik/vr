import tkinter as tk

from Core.LP.Runtime.LpBankProblemView import LpBankView


class BanksView(tk.Frame):
    def __init__(self, args, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)

        self.lp_bank = LpBankView(master=self, args=args)
        self.lp_bank.pack(fill=tk.BOTH, expand=True)
