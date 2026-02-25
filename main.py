from app import App
from tasks.task1 import Task1
from tasks.task2 import Task2

tasks = [
    Task1(variant=1),
    Task2(variant=1),
]

app = App(tasks)
app.mainloop()