from tkinter import *
from tkinter import ttk
import tkinter.font as tkFont

from util.filtered_words import chosen_word
from .settings import GameSettings


class WordleClone:
    def __init__(self, root):
        self.root = root
        self.settings = GameSettings()
        self.valid_clicks = 0
        self.toggle_var = IntVar()
        self.tries_labels = []
        self.setup_ui()

        self.CHOSEN_WORD = chosen_word(
            self.settings.word_length, 
            self.settings.has_recurring_letters
        ).upper()

        print(f'Chosen Word: {self.CHOSEN_WORD}')
    
    def setup_ui(self):
        self.root.title(self.settings.title)
        self.root.geometry(self.settings.window_size)

        # Main layout container
        self.mainframe = ttk.Frame(self.root, padding='3 3 12 12')
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Configure grid
        for i in range(2):
            self.mainframe.columnconfigure(i, weight=1)
            self.mainframe.rowconfigure(i, weight=1)
        
        self.setup_labels()
        self.setup_inputs()
        self.setup_settings_info()

    def setup_labels(self):
        self.labelframe = ttk.Frame(self.mainframe)
        self.labelframe.grid(column=2, row=0)
        self.labelframe['borderwidth'] = 1

        for row in range(self.settings.max_tries):
            row_labels = []
            for col in range(self.settings.word_length):
                label = ttk.Label(self.labelframe, text='_', font=('Arial', 12, 'bold'), width=2)
                label.grid(row=row, column=col, padx=1, pady=1, sticky='nsew')
                row_labels.append(label)
            self.tries_labels.append(row_labels)

    def setup_inputs(self):
        self.guess_input = StringVar()

        self.guess_entry = ttk.Entry(self.mainframe, width=10, textvariable=self.guess_input)
        self.guess_entry.grid(column=2, row=1, sticky=(W, E))
        self.guess_entry.focus()

        self.guess_button = ttk.Button(self.mainframe, text='Guess', command=self.check_guess)
        self.guess_button.grid(column=3, row=1, sticky=E)

        self.settings_button = ttk.Button(self.mainframe, text='⚙', command=self.open_settings_window)
        self.settings_button.grid(column=0, row=1)

    def setup_settings_info(self):
        self.setting_info_frame = ttk.Frame(self.mainframe)
        self.setting_info_frame.grid(column=0, row=0, sticky=(W, S))

        self.correct_label = ttk.Label(self.setting_info_frame, text=f'Correct: {self.settings.colors["correct"]}')
        self.correct_label.grid(column=0, row=0, sticky=W, padx=5)

        self.present_label = ttk.Label(self.setting_info_frame, text=f'Present: {self.settings.colors["present"]}')
        self.present_label.grid(column=0, row=1, sticky=W, padx=5)

        self.absent_label = ttk.Label(self.setting_info_frame, text=f'Absent: {self.settings.colors["absent"]}')
        self.absent_label.grid(column=0, row=2, sticky=W, padx=5)
        
        self.max_tries_label = ttk.Label(self.setting_info_frame, text=f'Max Tries: {self.settings.max_tries}')
        self.max_tries_label.grid(column=0, row=3, sticky=W, padx=5)
        
        self.word_length_label = ttk.Label(self.setting_info_frame, text=f'Word Length: {self.settings.word_length}')
        self.word_length_label.grid(column=0, row=4, sticky=W, padx=5)
        
        self.s_recurring_letters_label = ttk.Label(
            self.setting_info_frame, 
            text=f'Recurring Letters: {self.settings.has_recurring_letters}'
        )
        self.s_recurring_letters_label.grid(column=0, row=5, sticky=W, padx=5)

    def adjust_window_size(self):
        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_reqheight()
        root.geometry(f'{width}x{height}')

    def check_guess(self):
        guess_word = self.guess_input.get().upper()
        self.guess_entry.delete(0, END)

        for i, letter in enumerate(guess_word):
            if i < len(self.CHOSEN_WORD):
                color = (
                    self.settings.colors['correct'] if letter == self.CHOSEN_WORD[i]
                    else self.settings.colors['present'] if letter in self.CHOSEN_WORD
                    else self.settings.colors['absent']
                )

                self.tries_labels[self.valid_clicks][i].config(text=letter, foreground=color)
        
        self.valid_clicks += 1

        if guess_word == self.CHOSEN_WORD:
            self.open_popup(f'CONGRATULATIONS, YOU WON!!!\nThe word was {self.CHOSEN_WORD}')
            return

        if self.valid_clicks >= self.settings.max_tries:
            self.open_popup(f'GAME OVER\nThe word was {self.CHOSEN_WORD}')
            return

        self.guess_entry.focus()

    def open_popup(self, message: str):
        popup = Toplevel(self.root)
        popup.title('Popup Window')

        font_widget = tkFont.Font(font='TkDefaultFont')

        lines = message.split('\n')
        max_line_width = max(font_widget.measure(line) for line in lines) + 20
        height = 50 + (len(lines) * 20)

        popup.geometry(f'{max_line_width}x{height}')

        frame = ttk.Frame(popup)
        frame.pack(expand=True, fill='both')

        label = ttk.Label(frame, text=message, anchor='center', justify='center')
        label.pack(expand=True)

        restart_button = ttk.Button(popup, text='Restart', command=lambda: self.reset_game(popup))
        restart_button.pack(pady=10)

    
    def open_settings_window(self):
        settings_window = Toplevel(self.root)
        settings_window.title('Settings')
        settings_window.geometry('260x230')

        updated_settings = {
            'word_length': self.settings.word_length,
            'max_tries': self.settings.max_tries,
            'colors': self.settings.colors.copy(),
            'has_recurring_letters': self.settings.has_recurring_letters
        }

        def validate_input(new_value, min_val, max_val):
            # Check if the new_value is numeric and within the specified range
            if new_value.isdigit():
                value = int(new_value)
                if min_val <= value <= max_val:
                    return True
            return False

        # Register validation function
        def create_vcmd(min_val, max_val):
            return settings_window.register(lambda new_value: validate_input(new_value, min_val, max_val))

        # Word Length Option
        word_length_var = IntVar(value=self.settings.word_length)
        ttk.Label(settings_window, text='Word Length:').grid(row=0, column=0, sticky='w', padx=5, pady=5)
        word_length_vcmd = create_vcmd(3, 10)
        word_length_spinbox = ttk.Spinbox(
            settings_window, 
            from_=3, 
            to=10, 
            textvariable=word_length_var, 
            validate='key',
            validatecommand=(word_length_vcmd, '%P'),
            wrap=True,
            width=5
        )
        word_length_spinbox.grid(row=0, column=1, padx=5, pady=5, sticky=W)
        
        # Max Tries Option
        max_tries_var = IntVar(value=self.settings.max_tries)
        ttk.Label(settings_window, text='Max Tries:').grid(row=1, column=0, sticky='w', padx=5, pady=5)
        max_tries_vcmd = create_vcmd(1, 10)
        max_tries_spinbox = ttk.Spinbox(
            settings_window,
            from_=1,
            to=10,
            textvariable=max_tries_var,
            validate='key',
            validatecommand=(max_tries_vcmd, '%P'),
            wrap=True,
            width=5
        )
        max_tries_spinbox.grid(row=1, column=1, padx=5, pady=5, sticky=W)

        # Color Selection Dropdown
        color_options = ['Red', 'Blue', 'Green', 'Yellow', 'Purple', 'Orange', 'Cyan', 'Magenta', 'Gray', 'Black']  
        correct_color_var = StringVar(value=self.settings.colors['correct'] if self.settings.colors else color_options[0])
        present_color_var = StringVar(value=self.settings.colors['present'] if self.settings.colors else color_options[0])
        absent_color_var = StringVar(value=self.settings.colors['absent'] if self.settings.colors else color_options[0])

        def update_color(event, state, color_var):
            updated_settings['colors'][state] = color_var.get()

        ttk.Label(settings_window, text='Correct Color:').grid(row=2, column=0, sticky='w', padx=5, pady=5)
        correct_color_dropdown = ttk.Combobox(settings_window, textvariable=correct_color_var, values=color_options, state='readonly', width=7)
        correct_color_dropdown.grid(row=2, column=1, padx=5, pady=5, sticky=W)
        correct_color_dropdown.bind(
            '<<ComboboxSelected>>', 
            lambda event: update_color(
                event=event, 
                state='correct', 
                color_var=correct_color_var
            )
        )

        ttk.Label(settings_window, text='Present Color:').grid(row=3, column=0, sticky='w', padx=5, pady=5)
        present_color_dropdown = ttk.Combobox(settings_window, textvariable=present_color_var, values=color_options, state='readonly', width=7)
        present_color_dropdown.grid(row=3, column=1, padx=5, pady=5, sticky=W)
        present_color_dropdown.bind(
            '<<ComboboxSelected>>', 
            lambda event: update_color(
                event=event, 
                state='present',
                color_var=present_color_var
            )
        )

        ttk.Label(settings_window, text='Absent Color:').grid(row=4, column=0, sticky='w', padx=5, pady=5)
        absent_color_dropdown = ttk.Combobox(settings_window, textvariable=absent_color_var, values=color_options, state='readonly', width=7)
        absent_color_dropdown.grid(row=4, column=1, padx=5, pady=5, sticky=W)
        absent_color_dropdown.bind(
            '<<ComboboxSelected>>', 
            lambda event: update_color(
                event=event,
                state='absent',
                color_var=absent_color_var
            )
        )

        # Recurring Letters Toggle
        recurring_var = BooleanVar(value=self.settings.has_recurring_letters)
        def toggle_recurring():
            updated_settings['has_recurring_letters'] = recurring_var.get()

        ttk.Label(settings_window, text='Enable Recurring Letters').grid(row=5, column=0, sticky=W, padx=5, pady=5)
        ttk.Checkbutton(
            settings_window,  
            variable=recurring_var, 
            command=toggle_recurring
        ).grid(row=5, column=1, sticky=W, padx=5, pady=5)

        

        # Save Settings When Closed
        def apply_settings():
            updated_settings['word_length'] = word_length_var.get()
            updated_settings['max_tries'] = max_tries_var.get()
            updated_settings['has_recurring_letters'] = recurring_var.get()
            self.reset_game(settings_window, updated_settings)

        update_button = ttk.Button(settings_window, text='Update Settings', command=apply_settings)
        update_button.grid(row=6, column=0, columnspan=2, pady=10)



    def reset_game(self, window, updated_settings=None):
        window.destroy()

        self.valid_clicks = 0
        
        if updated_settings:
            self.settings.update_setting('max_tries', updated_settings['max_tries'])
            self.settings.update_setting('word_length', updated_settings['word_length'])
            self.settings.update_setting('has_recurring_letters', updated_settings['has_recurring_letters'])
            self.settings.update_setting('colors', updated_settings['colors'])

        # Update settings info 
        self.correct_label.config(text=f"Correct: {self.settings.colors['correct']}")
        self.present_label.config(text=f"Present: {self.settings.colors['present']}")
        self.absent_label.config(text=f"Absent: {self.settings.colors['absent']}")
        self.max_tries_label.config(text=f"Max Tries: {self.settings.max_tries}")
        self.word_length_label.config(text=f"Word Length: {self.settings.word_length}")
        self.s_recurring_letters_label.config(text=f"Recurring Letters: {self.settings.has_recurring_letters}")
        
        self.CHOSEN_WORD = chosen_word(
            self.settings.word_length, 
            self.settings.has_recurring_letters
        ).upper()
        print(f'Chosen Word: {self.CHOSEN_WORD}')

        for row in self.tries_labels:
            for label in row:
                label.destroy()
        
        self.tries_labels.clear()
        
        self.setup_labels()
        self.setup_inputs()
        self.adjust_window_size()

        
if __name__ == '__main__':
    root = Tk()
    app = WordleClone(root)
    root.mainloop()
