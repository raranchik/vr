import tkinter as tk


class ScrollableFrame(tk.Frame):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)

        self.canvas = tk.Canvas(self)
        self.container = tk.Frame(self.canvas)
        self.v_scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.h_scrollbar = tk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set)

        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas.create_window((0, 0), window=self.container, anchor=tk.NW)

        self._bind_frame_configure()
        self._bind_mouse_wheel()

    def get_container(self) -> tk.Frame:
        return self.container

    def focus(self):
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)
        self._bind_mouse_wheel()
        self._bind_frame_configure()

    def unfocus(self):
        self._unbind_mouse_wheel()
        self._unbind_frame_configure()

    def _bind_mouse_wheel(self):
        self.canvas.bind_all('<MouseWheel>', self._on_mouse_wheel)
        self.canvas.bind_all('<Button-4>', self._on_mouse_wheel)
        self.canvas.bind_all('<Button-5>', self._on_mouse_wheel)

    def _unbind_mouse_wheel(self):
        self.canvas.unbind_all('<MouseWheel>')
        self.canvas.unbind_all('<Button-4>')
        self.canvas.unbind_all('<Button-5>')

    def _bind_frame_configure(self):
        self.container.bind('<Configure>', self._on_frame_configure)

    def _unbind_frame_configure(self):
        self.container.bind('<Configure>', self._on_frame_configure)

    def _on_mouse_wheel(self, e):
        if e.delta:
            self.canvas.yview_scroll(int(-1 * (e.delta / 120)), tk.UNITS)
        elif e.num == 4:
            self.canvas.yview_scroll(-1, tk.UNITS)
        elif e.num == 5:
            self.canvas.yview_scroll(1, tk.UNITS)

    def _on_frame_configure(self, e):
        self.canvas.configure(scrollregion=self.canvas.bbox(tk.ALL))
