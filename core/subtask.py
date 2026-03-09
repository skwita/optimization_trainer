class Question:
    def __init__(self, text, answer, tolerance=0):
        self.text = text
        self.answer = answer
        self.tolerance = tolerance


class SubTask:
    def __init__(self, title, condition_elements, questions):
        self.title = title
        self.condition_elements = condition_elements
        self.questions = questions
        self.current_step = 0
        self.completed = False