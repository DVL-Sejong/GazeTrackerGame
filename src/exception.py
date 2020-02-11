class Error:
    def __init__(self):
        self.is_true = False
        self.message = ""

    def set_message(self, message):
        self.is_true = True
        self.message = message
