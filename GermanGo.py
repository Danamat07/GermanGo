import tkinter as tk
from tkinter import messagebox
import json
import random


class GermanGo:

    def __init__(self, master, words=None):
        self.next_button = None
        self.score_label = None
        self.submit_button = None
        self.answer_entry = None
        self.question_label = None
        self.title_label = None
        self.master = master
        self.words = words if words else []
        self.score = 0
        self.current_question = 0
        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(self.master, text="GermanGo! Learn german", font=("Arial", 18))
        self.title_label.pack(pady=20)
        self.question_label = tk.Label(self.master, text="What is the english translation of '----'?",
                                       font=("Arial", 14))
        self.question_label.pack(pady=10)
        self.answer_entry = tk.Entry(self.master, font=("Arial", 12))
        self.answer_entry.pack(pady=10)
        self.submit_button = tk.Button(self.master, text="Submit", command=self.check_answer, font=("Arial", 12))
        self.submit_button.pack(pady=20)
        self.score_label = tk.Label(self.master, text="Score: 0", font=("Arial", 12))
        self.score_label.pack(pady=10)
        self.next_button = tk.Button(self.master, text="Next", command=self.next_question, font=("Arial", 12))
        self.next_button.pack(pady=20)
        self.next_button.config(state="disabled")

    def read_from_file(self, file_path):
        try:
            with open(file_path, "r") as file:
                self.words = json.load(file)
            print(f"Loaded {len(self.words)} words from {file_path}.")
        except FileNotFoundError:
            messagebox.showerror("Error", f"File not found: {file_path}.")
        except json.JSONDecodeError:
            messagebox.showerror("Error", f"File {file_path} is not a valid JSON file.")

    def shuffle_words(self):
        random.shuffle(self.words)

    def start_quiz(self, file_path):
        self.read_from_file(file_path)
        if self.words:
            self.shuffle_words()
            self.display_question()

    def display_question(self):
        if self.current_question < 20:
            word = self.words[self.current_question]
            self.question_label.config(text=f"What is the english translation of '{word['german']}'?")
            self.answer_entry.delete(0, tk.END)
            self.submit_button.config(state="normal")
            self.next_button.config(state="disabled")
        else:
            self.end_quiz()

    def check_answer(self):
        user_answer = self.answer_entry.get().strip().lower()
        correct_answer = self.words[self.current_question]['english'].lower()
        if user_answer == correct_answer:
            self.score += 1
            messagebox.showinfo("Correct!", f"Correct! The translation is '{correct_answer}'.")
        else:
            messagebox.showinfo("Incorrect", f"Wrong! The correct answer is '{correct_answer}'.")

        self.score_label.config(text=f"Score: {self.score}")
        self.submit_button.config(state="disabled")
        self.next_button.config(state="normal")

    def next_question(self):
        self.current_question += 1
        self.display_question()

    def end_quiz(self):
        messagebox.showinfo("Quiz Complete", f"Quiz complete! Your score is {self.score}/20.")
        self.master.quit()


def main():
    root = tk.Tk()
    root.title("GermanGo")
    quiz = GermanGo(root)
    file_path = "dictionary.json"
    quiz.start_quiz(file_path)
    root.mainloop()


if __name__ == "__main__":
    main()
