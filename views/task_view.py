import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from core.checker import check_answer

class TaskView(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)

        self.app = app
        self.task = None
        self.current_subtask = None

        # ===== ROOT GRID =====
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # ===== SIDEBAR =====
        sidebar = ttk.Frame(self, padding=10)
        sidebar.grid(row=0, column=0, sticky="ns")
        sidebar.rowconfigure(1, weight=1)

        ttk.Label(sidebar, text="Подзадания", font=("Segoe UI", 14, "bold")).grid(row=0, column=0, pady=10)

        self.subtask_list = ttk.Treeview(sidebar, show="tree", height=20)
        self.subtask_list.grid(row=1, column=0, sticky="ns")
        self.subtask_list.bind("<<TreeviewSelect>>", self.select_subtask)

        ttk.Button(sidebar, text="← Назад", bootstyle=SECONDARY,
                   command=lambda: app.show("home")).grid(row=2, column=0, pady=10, sticky="ew")

        # ===== CONTENT AREA =====
        content = ttk.Frame(self, padding=(20, 20, 20, 20))
        content.grid(row=0, column=1, sticky="nsew")
        content.columnconfigure(0, weight=1)

        canvas = ttk.Canvas(content)
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(content, orient="vertical", command=canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        canvas.configure(yscrollcommand=scrollbar.set)
        self.condition_frame = ttk.Frame(canvas)

        canvas.create_window((0, 0), window=self.condition_frame, anchor="nw")
        self.condition_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        content.columnconfigure(0, weight=1)
        content.rowconfigure(0, weight=1)

        # вопрос
        self.question = ttk.Label(content, text="", font=("Segoe UI", 14, "bold"), justify=LEFT, anchor="nw")
        self.question.grid(row=1, column=0, sticky="ew", pady=(0, 15))

        # ===== INPUT AREA =====
        input_frame = ttk.Frame(content)
        input_frame.grid(row=2, column=0, sticky="ew")
        input_frame.columnconfigure(0, weight=1)

        self.entry = ttk.Entry(input_frame)
        self.entry.grid(row=0, column=0, sticky="ew", padx=(0, 5))

        ttk.Button(input_frame, text="Проверить", bootstyle=SUCCESS, command=self.check).grid(row=0, column=1)

        # ресайз
        self.bind("<Configure>", self.on_resize)

    # ============================
    # LOAD TASK
    # ============================
    def load_task(self, task):
        self.task = task
        self.current_subtask = None
        self.subtask_list.delete(*self.subtask_list.get_children())
        for i, st in enumerate(task.subtasks):
            self.subtask_list.insert("", "end", iid=str(i), text=st.title)
        self.clear_condition()
        self.question.config(text="")

    def clear_condition(self):
        for widget in self.condition_frame.winfo_children():
            widget.destroy()

    # ============================
    # SELECT SUBTASK
    # ============================
    def select_subtask(self, event):
        selection = self.subtask_list.selection()
        if not selection:
            return
        idx = selection[0]
        st = self.task.subtasks[int(idx)]
        self.current_subtask = st
        st.current_step = 0
        self.show_step()

    # ============================
    # SHOW STEP
    # ============================
    def show_step(self):
        st = self.current_subtask
        self.clear_condition()

        row_idx = 0
        for element in st.condition_elements:
            if element["type"] == "text":
                lbl = ttk.Label(self.condition_frame, text=element["value"], justify=LEFT, anchor="nw",
                                font=("Segoe UI", 12))
                lbl.grid(row=row_idx, column=0, sticky="ew", pady=5)
                row_idx += 1
            elif element["type"] == "table":
                table_data = element["value"]
                table = ttk.Treeview(self.condition_frame, columns=table_data["columns"], show="headings",
                                     height=len(table_data["data"]))
                for col in table_data["columns"]:
                    table.heading(col, text=col)
                    table.column(col, anchor="center", stretch=True)
                for row in table_data["data"]:
                    table.insert("", "end", values=row)
                table.grid(row=row_idx, column=0, sticky="ew", pady=5)
                row_idx += 1
            elif element["type"] == "formula":
                self.render_formula(
                    self.condition_frame,
                    element["value"],
                    row_idx
                )

                row_idx += 1

        # question
        q = st.questions[st.current_step]
        self.question.config(text=q.text)

    # ============================
    # CHECK ANSWER
    # ============================
    def check(self):
        if not self.current_subtask:
            return
        st = self.current_subtask
        q = st.questions[st.current_step]
        user = self.entry.get()
        if check_answer(user, q.answer, q.tolerance):
            st.current_step += 1
            self.entry.delete(0, END)
            if st.current_step >= len(st.questions):
                st.completed = True
                messagebox.showinfo("Готово", "Подзадание выполнено!")
                self.subtask_list.item(self.subtask_list.selection(), tags=("done",))
                self.subtask_list.tag_configure("done", background="#b8f2c8")
            else:
                self.show_step()
        else:
            messagebox.showerror("Ошибка", "Ответ неверный")

    # ============================
    # RESIZE
    # ============================
    def on_resize(self, event):
        try:
            width = event.width - 80
            if width < 200:
                width = 200
            # обновляем wraplength для всех Label в условии
            for widget in self.condition_frame.winfo_children():
                if isinstance(widget, ttk.Label):
                    widget.config(wraplength=width)
            self.question.config(wraplength=width)
        except:
            pass

    def render_formula(self, parent, latex, row):

        fig = plt.figure(figsize=(3, 0.3))
        fig.patch.set_alpha(0)
        fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

        plt.text(
            0.5,
            0.5,
            f"${latex}$",
            fontsize=12,
            ha="center",
            va="center"
        )

        plt.axis("off")

        canvas = FigureCanvasTkAgg(fig, master=parent)
        widget = canvas.get_tk_widget()

        widget.grid(row=row, column=0, sticky="w", pady=5)

        canvas.draw()