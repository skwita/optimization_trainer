import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from core.checker import check_answer


class TaskView(ttk.Frame):

    def __init__(self, parent, app):
        super().__init__(parent)

        self.bind("<Configure>", self.on_resize)
        self.app = app
        self.task = None
        self.current_subtask = None

        # ===== GRID ROOT =====
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # ===== SIDEBAR =====
        sidebar = ttk.Frame(self, padding=10)
        sidebar.grid(row=0, column=0, sticky="ns")

        sidebar.rowconfigure(1, weight=1)

        ttk.Label(
            sidebar,
            text="Подзадания",
            font=("Segoe UI", 14, "bold")
        ).grid(row=0, column=0, pady=10)

        self.subtask_list = ttk.Treeview(sidebar)
        self.subtask_list.grid(row=1, column=0, sticky="ns")

        self.subtask_list.bind(
            "<<TreeviewSelect>>",
            self.select_subtask
        )

        ttk.Button(
            sidebar,
            text="← Назад",
            bootstyle=SECONDARY,
            command=lambda: app.show("home")
        ).grid(row=2, column=0, pady=10, sticky="ew")

        # ===== CONTENT AREA =====
        content = ttk.Frame(self, padding=20)
        content.grid(row=0, column=1, sticky="nsew")
        content.columnconfigure(0, weight=1)
        content.rowconfigure(0, weight=1)

        # CONDITION BLOCK — адаптивный wraplength
        self.condition = ttk.Label(
            content,
            text="",
            justify=LEFT,
            font=("Segoe UI", 12),
            anchor="nw",  # верхний левый угол
        )
        self.condition.grid(row=0, column=0, sticky="nsew", pady=(0, 15))

        # QUESTION — адаптивный wraplength
        self.question = ttk.Label(
            content,
            text="",
            font=("Segoe UI", 14, "bold"),
            justify=LEFT,
            anchor="nw"
        )
        self.question.grid(row=1, column=0, sticky="nsew", pady=(0, 15))

        # INPUT AREA
        input_frame = ttk.Frame(content)
        input_frame.grid(row=2, column=0, sticky="ew")
        input_frame.columnconfigure(0, weight=1)

        self.entry = ttk.Entry(input_frame)
        self.entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))

        ttk.Button(
            input_frame,
            text="Проверить",
            bootstyle=SUCCESS,
            command=self.check
        ).grid(row=0, column=1)

        self.bind("<Configure>", self.on_resize)

    # =========================

    def on_resize(self, event):
        padding_lr = 40  # padding слева + справа
        new_width = event.width - padding_lr * 7
        if new_width < 50:
            new_width = 50
        self.condition.config(wraplength=new_width)
        self.question.config(wraplength=new_width)

    def load_task(self, task):

        self.task = task
        self.current_subtask = None

        self.subtask_list.delete(
            *self.subtask_list.get_children()
        )

        for i, st in enumerate(task.subtasks):
            self.subtask_list.insert(
                "",
                "end",
                iid=str(i),
                text=st.title
            )

        self.condition.config(text="")
        self.question.config(text="")

    def select_subtask(self, event):

        selection = self.subtask_list.selection()

        if not selection:
            return

        idx = selection[0]

        st = self.task.subtasks[int(idx)]

        self.current_subtask = st
        st.current_step = 0

        self.show_step()

    def show_step(self):

        st = self.current_subtask

        self.condition.config(text=st.condition)

        q = st.questions[st.current_step]
        self.question.config(text=q.text)

    def check(self):

        st = self.current_subtask
        q = st.questions[st.current_step]

        user = self.entry.get()

        if check_answer(user, q.answer, q.tolerance):

            st.current_step += 1
            self.entry.delete(0, END)

            if st.current_step >= len(st.questions):

                st.completed = True

                messagebox.showinfo(
                    "Готово",
                    "Подзадание выполнено!"
                )

                self.subtask_list.item(
                    self.subtask_list.selection(),
                    tags=("done",)
                )

                self.subtask_list.tag_configure(
                    "done",
                    background="#b8f2c8"
                )

            else:
                self.show_step()

        else:
            messagebox.showerror(
                "Ошибка",
                "Ответ неверный"
            )