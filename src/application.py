import tkinter as tk
from src.utils import generate_random_nums, format_equation
import time


class MathQuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Math Quiz")

        # Default settings
        self.low = 2
        self.max_num = 10
        self.num_factors = 2

        # Initialize counters:
        self.correct_answers = 0
        self.answer_times = []  # List to store times for each question
        self.quick_answers = []  # Store quick answers (answered quickly)
        self.slow_answers = []  # Store slow answers (answered slowly)
        self.incorrect_answers = []  # Store incorrect answers (answered wrong)

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
        self.first_question = True  # Flag to check if it's the first question
        self.timer_start_time = time.time()  # Start the global timer for the app

        # Set initial countdown time (5 minutes = 300 seconds)
        self.countdown_time = 300
        self.update_timer()

    def create_widgets(self):
        # Timer label (top-left corner)
        self.timer_label = tk.Label(self.root, text="Time: 5:00", font=("Arial", 14))
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
            if prediction == self.answer:
                self.correct_answers += 1
                self.counter_label.config(
                    text=f"Correct answers: {self.correct_answers}"
                )

                # Calculate time taken for this answer
                time_taken = time.time() - self.start_time
                if time_taken < 5:  # Quick answer
                    self.quick_answers.append((self.input_str, time_taken))
                else:  # Slow answer
                    self.slow_answers.append((self.input_str, time_taken))

                self.next_question()
            else:
                self.incorrect_answers.append(
                    (self.input_str, self.answer)
                )  # Store incorrect answers
                self.label.config(text="Wrong! Try again.")
                # After 0.5 seconds, revert to the original equation
                self.root.after(500, self.reset_label)
                # Clear input box after each attempt
                self.entry.delete(0, tk.END)
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
        # Display results for quick and slow answers
        result_window = tk.Toplevel(self.root)
        result_window.title("Answer Times")

        quick_frame = tk.LabelFrame(
            result_window, text="Quick Answers", font=("Arial", 12)
        )
        quick_frame.pack(pady=10, padx=10)

        slow_frame = tk.LabelFrame(
            result_window, text="Slow Answers", font=("Arial", 12)
        )
        slow_frame.pack(pady=10, padx=10)

        incorrect_frame = tk.LabelFrame(
            result_window, text="Incorrect Answers", font=("Arial", 12)
        )
        incorrect_frame.pack(pady=10, padx=10)

        # Display quick answers
        for eq, time_taken in self.quick_answers:
            label = tk.Label(
                quick_frame, text=f"{eq} - Time: {time_taken:.2f}s", font=("Arial", 10)
            )
            label.pack()

        # Display slow answers
        for eq, time_taken in self.slow_answers:
            label = tk.Label(
                slow_frame, text=f"{eq} - Time: {time_taken:.2f}s", font=("Arial", 10)
            )
            label.pack()

        # Display incorrect answers
        for eq, correct_answer in self.incorrect_answers:
            label = tk.Label(
                incorrect_frame,
                text=f"{eq} - Correct Answer: {correct_answer}",
                font=("Arial", 10),
            )
            label.pack()


def train():
    # Create the main window
    root = tk.Tk()

    # Set structure:
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

    # Instantiate the MathQuizApp class
    app = MathQuizApp(root)
    # Run the GUI main loop
    root.mainloop()