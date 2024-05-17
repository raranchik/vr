import tkinter as tk

CONTAINER_TAG = 'container'


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

        self.canvas.create_window((0, 0), window=self.container, anchor=tk.NW, tags=CONTAINER_TAG)

        self.mouse_wheel_binds = None
        self.__frame_configure_bind = None
        self.__resize_container_bind = None

        self.__bind_frame_configure()
        self.__bind_resize_container()

    def get_container(self) -> tk.Frame:
        return self.container

    def focus(self):
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)
        self.__bind_mouse_wheel()

    def unfocus(self):
        self.__unbind_mouse_wheel()

    def __bind_mouse_wheel(self):
        if self.mouse_wheel_binds is not None:
            return

        self.mouse_wheel_binds = []

        bind = self.canvas.bind_all('<MouseWheel>', self._on_mouse_wheel)
        self.mouse_wheel_binds.append(('<MouseWheel>', bind))

        bind = self.canvas.bind_all('<Button-4>', self._on_mouse_wheel)
        self.mouse_wheel_binds.append(('<Button-4>', bind))

        bind = self.canvas.bind_all('<Button-5>', self._on_mouse_wheel)
        self.mouse_wheel_binds.append(('<Button-5>', bind))

    def __unbind_mouse_wheel(self):
        if self.mouse_wheel_binds is None:
            return

        for bind in self.mouse_wheel_binds:
            self.canvas.unbind(bind[0], bind[1])

        self.mouse_wheel_binds = None

    def __bind_frame_configure(self):
        if self.__frame_configure_bind is not None:
            return

        self.__frame_configure_bind = self.container.bind('<Configure>', self.__on_frame_configure)

    def __unbind_frame_configure(self):
        if self.__frame_configure_bind is None:
            return

        self.container.unbind('<Configure>', self.__frame_configure_bind)
        self.__frame_configure_bind = None

    def __bind_resize_container(self):
        if self.__resize_container_bind is not None:
            return

        self.__resize_container_bind = self.canvas.bind('<Configure>', self.__on_resize_container)

    def __unbind_resize_container(self):
        if self.__resize_container_bind is None:
            return

        self.canvas.unbind('<Configure>', self.__resize_container_bind)
        self.__resize_container_bind = None

    def _on_mouse_wheel(self, e):
        if e.delta:
            self.canvas.yview_scroll(int(-1 * (e.delta / 120)), tk.UNITS)
        elif e.num == 4:
            self.canvas.yview_scroll(-1, tk.UNITS)
        elif e.num == 5:
            self.canvas.yview_scroll(1, tk.UNITS)

    def __on_frame_configure(self, e):
        self.canvas.configure(scrollregion=self.canvas.bbox(tk.ALL))

    def __on_resize_container(self, e):
        self.canvas.itemconfigure(CONTAINER_TAG, width=e.width)
