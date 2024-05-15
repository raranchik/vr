import tkinter as tk
from Core.ScrollableFrame import ScrollableFrame


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("VR")
        self.setup_window()

        frame = ScrollableFrame(self)
        frame.pack(fill=tk.BOTH, expand=True)
        for i in range(20):
            for j in range(20):
                lbl = tk.Label(frame.get_container(), text=f"Label {i}")
                lbl.grid(column=i, row=j)

    def setup_window(self):
        window_width = 400
        window_height = 400

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.geometry(f"{window_width}x{window_height}+{x}+{y}")


if __name__ == "__main__":
    app = App()
    app.mainloop()
