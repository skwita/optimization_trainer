class TaskBase:
    name = "Base Task"

    def __init__(self, variant=1):
        self.variant = variant
        self.subtasks = self.load_variant(variant)

    def load_variant(self, variant):
        raise NotImplementedError