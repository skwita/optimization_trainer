from app import App
from tasks.task1 import Task1
from tasks.task2 import Task2
from tasks.task3 import Task3
from tasks.task4 import Task4
from tasks.task5 import Task5
from tasks.task6 import Task6
from tasks.task7 import Task7
from tasks.task8 import Task8

tasks = [
    Task1(variant=1),
    Task2(variant=1),
    Task3(variant=1),
    Task4(variant=1),
    Task5(variant=1),
    Task6(variant=1),
    Task7(variant=1),
    Task8(variant=1),
]

app = App(tasks)
app.mainloop()