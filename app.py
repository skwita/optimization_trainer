import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from views.home_view import HomeView
from views.task_view import TaskView


class App(ttk.Window):

    def __init__(self, tasks):

        super().__init__(themename="cosmo")

        self.title("Практикум по методам оптимизации")
        self.geometry("1100x700")

        # ⭐ окно адаптивное
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.tasks = tasks

        self.container = ttk.Frame(self)
        self.container.grid(row=0, column=0, sticky="nsew")

        self.container.rowconfigure(0, weight=1)
        self.container.columnconfigure(0, weight=1)

        self.frames = {}

        self.frames["home"] = HomeView(self.container, self)
        self.frames["task"] = TaskView(self.container, self)

        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky="nsew")

        self.show("home")

    def show(self, name):
        self.frames[name].tkraise()