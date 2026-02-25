import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class HomeView(ttk.Frame):

    def __init__(self, parent, app):
        super().__init__(parent)

        self.app = app

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        title = ttk.Label(
            self,
            text="Практикум по методам оптимизации",
            font=("Segoe UI", 24, "bold")
        )
        title.grid(row=0, column=0, pady=40)

        buttons = ttk.Frame(self)
        buttons.grid(row=1, column=0, sticky="n")

        buttons.columnconfigure(0, weight=1)

        for i, task in enumerate(app.tasks):
            ttk.Button(
                buttons,
                text=task.name,
                bootstyle=PRIMARY,
                width=30,
                command=lambda t=task: self.open_task(t)
            ).grid(row=i, column=0, pady=8, sticky="ew")

    def open_task(self, task):
        self.app.frames["task"].load_task(task)
        self.app.show("task")