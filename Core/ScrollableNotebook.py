import tkinter
from tkinter import *
from tkinter import ttk
from Core.Event import Event as e_notifier


class ScrollableNotebook(ttk.Frame):
    def __init__(self, parent, enable_wheel_scroll=False, tab_menu=False, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args)
        self.on_tab_changed_event = e_notifier()

        self.x_pos = 0

        self.notebook_content = ttk.Notebook(self, **kwargs)
        self.notebook_content.pack(fill=tkinter.BOTH, expand=True)

        self.notebook_tab = ttk.Notebook(self, **kwargs)
        self.notebook_tab.bind("<<NotebookTabChanged>>", self.__on_tab_changed)

        if enable_wheel_scroll:
            self.notebook_tab.bind("<MouseWheel>", self.__on_wheel_scroll)

        slide_frame = ttk.Frame(self)
        slide_frame.place(relx=1.0, x=0, y=1, anchor=NE)
        self.menuSpace = 30
        if tab_menu:
            self.menuSpace = 50
            bottom_tab = ttk.Label(slide_frame, text="\u2630")
            bottom_tab.bind("<ButtonPress-1>", self.__on_press_bottom_menu)
            bottom_tab.pack(side=RIGHT)

        left_arrow = ttk.Label(slide_frame, text=" \u276E")
        left_arrow.bind("<ButtonPress-1>", self.__left_slide_start)
        left_arrow.bind("<ButtonRelease-1>", self.__on_release_slide_stop)
        left_arrow.pack(side=LEFT)

        right_arrow = ttk.Label(slide_frame, text=" \u276F")
        right_arrow.bind("<ButtonPress-1>", self.__on_press_right_slide_start)
        right_arrow.bind("<ButtonRelease-1>", self.__on_release_slide_stop)
        right_arrow.pack(side=RIGHT)

        self.notebook_content.bind("<Configure>", self.__on_content_configure_reset_slide)

        self.contents_managed = []
        self.timer = None

    def __on_wheel_scroll(self, e):
        if e.delta > 0:
            self.__scroll_left_slide(e)
        else:
            self.__scroll_right_slide(e)

    def __on_press_bottom_menu(self, e):
        tab_list_menu = Menu(self, tearoff=0)
        for tab in self.notebook_tab.tabs():
            tab_list_menu.add_command(label=self.notebook_tab.tab(tab, option="text"),
                                      command=lambda temp=tab: self.select(temp))
        try:
            tab_list_menu.tk_popup(e.x_root, e.y_root)
        finally:
            tab_list_menu.grab_release()

    def __on_tab_changed(self, e):
        try:
            self.notebook_content.select(self.notebook_tab.index("current"))
            self.on_tab_changed_event.notify(e=e)
        except:
            pass

    def __on_press_right_slide_start(self, e=None):
        if self.__scroll_right_slide(e):
            self.timer = self.after(100, self.__on_press_right_slide_start)

    def __scroll_right_slide(self, e):
        if self.notebook_tab.winfo_width() > self.notebook_content.winfo_width() - self.menuSpace:
            if (self.notebook_content.winfo_width() - (
                    self.notebook_tab.winfo_width() + self.notebook_tab.winfo_x())) <= self.menuSpace + 5:
                self.x_pos -= 20
                self.notebook_tab.place(x=self.x_pos, y=0)
                return True
        return False

    def __left_slide_start(self, e=None):
        if self.__scroll_left_slide(e):
            self.timer = self.after(100, self.__left_slide_start)

    def __scroll_left_slide(self, e):
        if not self.notebook_tab.winfo_x() == 0:
            self.x_pos += 20
            self.notebook_tab.place(x=self.x_pos, y=0)
            return True
        return False

    def __on_release_slide_stop(self, e):
        if self.timer != None:
            self.after_cancel(self.timer)
            self.timer = None

    def __on_content_configure_reset_slide(self, e=None):
        self.notebook_tab.place(x=0, y=0)
        self.x_pos = 0

    def get_selected_tab_id(self):
        if self.notebook_tab.select() == '':
            return -1

        return self.notebook_tab.index(self.notebook_tab.select())

    def add(self, frame, **kwargs):
        if len(self.notebook_tab.winfo_children()) != 0:
            self.notebook_content.add(frame, text="", state="hidden")
        else:
            self.notebook_content.add(frame, text="")
        self.notebook_tab.add(ttk.Frame(self.notebook_tab), **kwargs)
        self.contents_managed.append(frame)

    def forget(self, tab_id):
        index = self.notebook_tab.index(tab_id)
        self.notebook_content.forget(self.__get_content_tab_id(tab_id))
        self.notebook_tab.forget(tab_id)
        self.contents_managed[index].destroy()
        self.contents_managed.pop(index)

    def hide(self, tab_id):
        self.notebook_content.hide(self.__get_content_tab_id(tab_id))
        self.notebook_tab.hide(tab_id)

    def identify(self, x, y):
        return self.notebook_tab.identify(x, y)

    def index(self, tab_id):
        return self.notebook_tab.index(tab_id)

    def __get_content_tab_id(self, tab_id):
        return self.notebook_content.tabs()[self.notebook_tab.tabs().index(tab_id)]

    def insert(self, pos, frame, **kwargs):
        self.notebook_content.insert(pos, frame, **kwargs)
        self.notebook_tab.insert(pos, frame, **kwargs)

    def select(self, tab_id):
        self.notebook_tab.select(tab_id)

    def tab(self, tab_id, option=None, **kwargs):
        kwargs_content = kwargs.copy()
        kwargs_content["text"] = ""  # important
        self.notebook_content.tab(self.__get_content_tab_id(tab_id), option=None, **kwargs_content)
        return self.notebook_tab.tab(tab_id, option=None, **kwargs)

    def tabs(self):
        return self.notebook_tab.tabs()

    def enable_traversal(self):
        self.notebook_content.enable_traversal()
        self.notebook_tab.enable_traversal()

    def add_tab_changed_listener(self, callback):
        self.on_tab_changed_event.subscribe(callback)

    def remove_tab_changed_listener(self, callback):
        self.on_tab_changed_event.unsubscribe(callback)
