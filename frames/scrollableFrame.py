from tkinter import ttk, NSEW, Canvas

class ScrollableFrame(ttk.Frame):
    def __init__(self, width, height, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.canvas = Canvas(self)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set, width=width, height=height)
        self.canvas.grid(row=0, column=0, sticky=NSEW, padx=(4, 0), pady=4)
        self.scrollbar.grid(row=0, column=1, sticky=NSEW, padx=(0, 4), pady=4)
        self.scrollable_frame.bind('<Enter>', self.bindMouseWheel)
        self.scrollable_frame.bind('<Leave>', self.unbindMouseWheel)

    def bindMouseWheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self.onMouseWheel)

    def unbindMouseWheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def onMouseWheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
