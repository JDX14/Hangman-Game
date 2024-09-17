import tkinter as tk
from tkinter import messagebox
import random
import requests

class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game")
        
        #Hangman display
        self.hangman_stages = [
            '''
               ------
               |    |
               |
               |
               |
               |
               |
            --------
            ''',
            '''
               ------
               |    |
               |    O
               |
               |
               |
               |
            --------
            ''',
            '''
               ------
               |    |
               |    O
               |    |
               |
               |
               |
            --------
            ''',
            '''
               ------
               |    |
               |    O
               |   /|
               |
               |
               |
            --------
            ''',
            '''
               ------
               |    |
               |    O
               |   /|\\
               |
               |
               |
            --------
            ''',
            '''
               ------
               |    |
               |    O
               |   /|\\
               |   /
               |
               |
            --------
            ''',
            '''
               ------
               |    |
               |    O
               |   /|\\
               |   / \\
               |
               |
            --------
            '''
        ]
        
        self.word = self.get_random_word()
        self.guesses = ''
        self.turns = len(self.hangman_stages) - 1  #Corresponding to hangman stages
        
        #Hangman display label
        self.hangman_label = tk.Label(self.root, text=self.hangman_stages[0], font=("Courier", 16), justify="left")
        self.hangman_label.pack(pady=10)
        
        #Word display
        self.word_label = tk.Label(self.root, text="_ " * len(self.word), font=("Arial", 24))
        self.word_label.pack(pady=20)
        
        #Turns left display
        self.turns_label = tk.Label(self.root, text=f"Turns left: {self.turns}", font=("Arial", 16))
        self.turns_label.pack(pady=10)
        
        #Input field for guessing
        self.entry = tk.Entry(self.root, font=("Arial", 14))
        self.entry.pack(pady=10)
        self.entry.bind("<Return>", self.guess_letter)  # Bind 'Enter' key to the guess_letter function
        
        #Guess button
        self.guess_button = tk.Button(self.root, text="Guess", command=self.guess_letter, font=("Arial", 14))
        self.guess_button.pack(pady=10)
        
        #Reset button, disabled at the start
        self.reset_button = tk.Button(self.root, text="Play Again", command=self.reset_game, font=("Arial", 14))
        self.reset_button.pack(pady=10)
        self.reset_button.config(state="disabled")
    
    #Get random word using the API
    def get_random_word(self):
        response = requests.get("https://random-word-api.herokuapp.com/word?number=1")
        word = response.json()[0]
        return word.lower()

    #Handle the player's guess
    def guess_letter(self, event=None):
        guess = self.entry.get().lower()
        self.entry.delete(0, tk.END)
        
        if len(guess) != 1 or not guess.isalpha():
            messagebox.showwarning("Invalid Input", "Please enter a single letter!")
            return
        
        if guess in self.guesses:
            messagebox.showwarning("Invalid Input", "You have already guessed that letter!")
            return
        
        self.guesses += guess
        
        #Wrong guess logic
        if guess not in self.word:
            self.turns -= 1
            self.hangman_label.config(text=self.hangman_stages[len(self.hangman_stages) - self.turns - 1])
            self.turns_label.config(text=f"Turns left: {self.turns}")
            if self.turns == 0:
                self.end_game(f"The word was: {self.word}")
                return

        self.update_word_display()
        
        #Check for win
        if "_" not in self.word_label.cget("text"):
            self.end_game(f"You Win! The word is: {self.word}")
    
    #Update word display after a guess
    def update_word_display(self):
        display_word = ""
        for char in self.word:
            if char in self.guesses:
                display_word += char + " "
            else:
                display_word += "_ "
        self.word_label.config(text=display_word.strip())
    
    #End game and disable further guesses
    def end_game(self, result_message):
        messagebox.showinfo("Game Over", result_message)
        self.guess_button.config(state="disabled")
        self.reset_button.config(state="normal")
    
    #Reset game 
    def reset_game(self):
        self.word = self.get_random_word()
        self.guesses = ''
        self.turns = len(self.hangman_stages) - 1
        self.hangman_label.config(text=self.hangman_stages[0])
        self.turns_label.config(text=f"Turns left: {self.turns}")
        self.word_label.config(text="_ " * len(self.word))
        self.guess_button.config(state="normal")
        self.reset_button.config(state="disabled")

# Main Program
if __name__ == "__main__":
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()