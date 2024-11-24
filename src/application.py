import tkinter as tk
from tkinter import messagebox
from src.utils import generate_random_nums, format_equation
import time


class SettingsWindow:
    def __init__(self):
        self.settings_root = tk.Tk()
        self.settings_root.title("Math Quiz Settings")

        # Set window size and position
        window_width = 300
        window_height = 200
        screen_width = self.settings_root.winfo_screenwidth()
        screen_height = self.settings_root.winfo_screenheight()
        position_top = int((screen_height - window_height) / 2)
        position_left = int((screen_width - window_width) / 2)
        self.settings_root.geometry(
            f"{window_width}x{window_height}+{position_left}+{position_top}"
        )

        # Variables to store settings
        self.low_var = tk.StringVar(value="2")
        self.high_var = tk.StringVar(value="10")
        self.settings = None

        self.create_settings_widgets()

    def create_settings_widgets(self):
        # Title
        title_label = tk.Label(
            self.settings_root, text="Quiz Settings", font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)

        # Frame for number range settings
        settings_frame = tk.Frame(self.settings_root)
        settings_frame.pack(pady=10)

        # Lowest number setting
        low_label = tk.Label(settings_frame, text="Lowest number:", font=("Arial", 12))
        low_label.grid(row=0, column=0, padx=5, pady=5)

        low_entry = tk.Entry(settings_frame, textvariable=self.low_var, width=10)
        low_entry.grid(row=0, column=1, padx=5, pady=5)

        # Highest number setting
        high_label = tk.Label(
            settings_frame, text="Highest number:", font=("Arial", 12)
        )
        high_label.grid(row=1, column=0, padx=5, pady=5)

        high_entry = tk.Entry(settings_frame, textvariable=self.high_var, width=10)
        high_entry.grid(row=1, column=1, padx=5, pady=5)

        # Start button
        start_button = tk.Button(
            self.settings_root,
            text="Start Quiz",
            command=self.start_quiz,
            font=("Arial", 12),
            width=15,
        )
        start_button.pack(pady=20)

    def validate_settings(self):
        try:
            low = int(self.low_var.get())
            high = int(self.high_var.get())

            if low < 1:
                messagebox.showerror("Error", "Lowest number must be at least 1")
                return False
            if high <= low:
                messagebox.showerror(
                    "Error", "Highest number must be greater than lowest number"
                )
                return False
            return True
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")
            return False

    def start_quiz(self):
        if self.validate_settings():
            self.settings = {
                "low": int(self.low_var.get()),
                "high": int(self.high_var.get()) + 1,  # 0-indexed :)
            }
            self.settings_root.destroy()

    def get_settings(self):
        self.settings_root.mainloop()
        return self.settings


class MathQuizApp:
    def __init__(self, root, settings):
        self.root = root
        self.root.title("Math Quiz")

        # Use settings from SettingsWindow
        self.low = settings["low"]
        self.max_num = settings["high"]
        self.num_factors = 2

        # Initialize counters
        self.correct_answers = 0
        self.incorrect_answers = []
        self.total_questions = 0

        # Ensure at least 2 numbers for multiplication
        assert self.num_factors > 1, "Need to multiply at least 2 numbers!"

        # Generate random numbers and their product
        self.random_nums, self.answer = generate_random_nums(
            low=self.low, high=self.max_num, num_factors=self.num_factors
        )

        # Generate the equation string
        self.input_str = format_equation(self.random_nums)

        # Set up the UI elements
        self.create_widgets()

        # Initialize start_time as None initially
        self.start_time = None
        self.first_question = True
        self.timer_start_time = time.time()

        self.countdown_time = 300
        self.update_timer()

    def create_widgets(self):
        # Timer label (top-left corner)
        self.timer_label = tk.Label(self.root, text="Time: 10:00", font=("Arial", 14))
        self.timer_label.place(x=10, y=10)

        # Counter label for correct answers (top-right corner)
        self.counter_label = tk.Label(
            self.root, text="Correct answers: 0", font=("Arial", 20)
        )
        self.counter_label.place(x=400, y=10)  # Top-right corner

        # Label to display the equation (centered)
        self.label = tk.Label(self.root, text=self.input_str, font=("Arial", 40))
        self.label.pack(pady=50)  # Add more padding to center it vertically

        # Entry widget for user input (centered below the equation)
        self.entry = tk.Entry(self.root, font=("Arial", 48), width=10)
        self.entry.pack(pady=10)

        # Button to display the results (positioned at the bottom-left)
        self.result_button = tk.Button(
            self.root,
            text="Show Results",
            font=("Arial", 14),
            command=self.show_results,
        )
        self.result_button.place(x=10, y=350)  # Bottom-left corner

        # Bind the Enter key to check the answer
        self.entry.bind("<Return>", self.check_answer)

    def update_timer(self):
        # Calculate the remaining time
        minutes = self.countdown_time // 60
        seconds = self.countdown_time % 60
        self.timer_label.config(text=f"Time: {minutes:02d}:{seconds:02d}")

        # Decrease countdown time every second
        if self.countdown_time > 0:
            self.countdown_time -= 1
            self.root.after(1000, self.update_timer)
        else:
            self.timer_label.config(text="Time's up!")
            self.show_results()  # Automatically show results when time is up

    def check_answer(self, event):
        try:
            # Start the timer only when the first question is asked
            if self.start_time is None:
                self.start_time = time.time()  # Start the timer on the first question
                self.first_question = (
                    False  # After the first question is shown, set the flag to False
                )

            # Get user input and validate
            prediction = float(self.entry.get())
            self.total_questions += 1

            if prediction == self.answer:
                self.correct_answers += 1
                self.counter_label.config(
                    text=f"Correct answers: {self.correct_answers}"
                )

            else:
                self.incorrect_answers.append(
                    (self.input_str, self.answer)
                )  # Store incorrect answers

            self.next_question()

        except ValueError:
            self.label.config(text="Enter a valid number.")
            self.root.after(500, self.reset_label)
            # Clear input box after each attempt
            self.entry.delete(0, tk.END)

    def reset_label(self):
        # Reset the label to the equation after 0.5 seconds
        self.label.config(text=self.input_str)

    def next_question(self):
        # Hide the input box after each attempt and show it again for the next question
        self.entry.pack_forget()
        self.show_input()

    def show_input(self):
        # Generate new random numbers and update the equation
        self.random_nums, self.answer = generate_random_nums(
            low=self.low, high=self.max_num, num_factors=self.num_factors
        )
        self.input_str = format_equation(self.random_nums)
        self.label.config(text=self.input_str)  # Update the equation display
        self.entry.pack(pady=10)  # Show the entry widget for the next question
        self.entry.delete(0, tk.END)  # Clear the entry widget

        # Set a new start time for the next question
        self.start_time = time.time()  # Start timing for the next question

    def show_results(self):
        # Calculate the percentage of correct answers
        if self.total_questions > 0:
            correct_percentage = (self.correct_answers / self.total_questions) * 100
        else:
            correct_percentage = 0

        # Display results for quick and slow answers
        result_window = tk.Toplevel(self.root)
        result_window.title("Results")

        results_label = tk.Label(
            result_window,
            text=f"Total Questions: {self.total_questions}\n"
            f"Correct Answers: {self.correct_answers}\n"
            f"Percentage: {correct_percentage:.2f}%",
            font=("Arial", 14),
        )
        results_label.pack(pady=20)

        incorrect_frame = tk.LabelFrame(
            result_window, text="Incorrect Answers", padx=10, pady=10
        )
        incorrect_frame.pack(pady=10)

        for eq, ans in self.incorrect_answers:
            incorrect_label = tk.Label(
                incorrect_frame, text=f"{eq} = {ans}", font=("Arial", 12)
            )
            incorrect_label.pack()

        retry_button = tk.Button(
            result_window,
            text="Retry",
            font=("Arial", 14),
            command=lambda: self.retry_del(result_window),  # Pass result_window safely
        )
        retry_button.pack(pady=20)

    def retry_del(self, result_window):
        # Ensure the window is not already destroyed
        if result_window.winfo_exists():
            result_window.destroy()  # Destroy the result window safely

        # Reset the application to retry the quiz
        self.correct_answers = 0
        self.incorrect_answers = []
        self.total_questions = 0
        self.countdown_time = 300
        self.update_timer()  # Update the timer if necessary
        self.show_input()  # Display the input for the first question
        self.counter_label.config(text=f"Correct answers: {self.correct_answers}")


def train():
    # First show settings window
    settings_window = SettingsWindow()
    settings = settings_window.get_settings()

    # If settings window was closed without clicking Start Quiz
    if settings is None:
        return

    # Create the main window
    root = tk.Tk()

    # Set structure
    window_width = 600
    window_height = 400
    root.geometry(f"{window_width}x{window_height}")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate the position to center the window
    position_top = int((screen_height - window_height) / 2)
    position_left = int((screen_width - window_width) / 2)

    # Set the window position to the center of the screen
    root.geometry(f"{window_width}x{window_height}+{position_left}+{position_top}")

    # Instantiate the MathQuizApp class with settings
    app = MathQuizApp(root, settings)
    # Run the GUI main loop
    root.mainloop()
