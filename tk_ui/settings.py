class GameSettings:
    def __init__(self):
        self.title = "Guess the Word"
        self.window_size = "400x200"
        self.max_tries = 5
        self.word_length = 5
        self.has_recurring_letters = False

        self.colors = {
            'correct': 'green',
            'present': 'orange',
            'absent': 'black'
        }

    def toggle_recurring_letters(self):
        self.has_recurring_letters = not self.has_recurring_letters

    def update_setting(self, key, value):
        if hasattr(self, key):
            setattr(self, key, value)
