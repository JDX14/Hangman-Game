import tkinter as tk
from tkinter import messagebox
import requests

class HangmanGame:
    def __init__(self, root):
        # Initialize the main window, game variables, and create GUI elements
        self.root = root
        self.root.title("Hangman Game")
        
        # Get a random word for the game
        self.word = self.get_random_word()
        self.guesses = ''
        self.turns = 12  # Set the number of turns the player starts with

        # Create label to display the word with blanks for unguessed letters
        self.word_label = tk.Label(self.root, text="_ " * len(self.word), font=("Arial", 24))
        self.word_label.pack(pady=20)

        # Create label to show the remaining number of turns
        self.turns_label = tk.Label(self.root, text=f"Turns left: {self.turns}", font=("Arial", 16))
        self.turns_label.pack(pady=10)

        # Create an entry field for the player to type their guesses
        self.entry = tk.Entry(self.root, font=("Arial", 14))
        self.entry.pack(pady=10)
        # Bind the Enter key to trigger the guess_letter function
        self.entry.bind("<Return>", self.guess_letter)

        # Create a button for submitting a guess
        self.guess_button = tk.Button(self.root, text="Guess", command=self.guess_letter, font=("Arial", 14))
        self.guess_button.pack(pady=10)

        # Create a button to restart the game
        self.reset_button = tk.Button(self.root, text="Play Again", command=self.reset_game, font=("Arial", 14))
        self.reset_button.pack(pady=10)
        self.reset_button.config(state="disabled")  # Disable the reset button until the game ends

    def get_random_word(self):
        # Fetch a random word from an online API
        response = requests.get("https://random-word-api.herokuapp.com/word?number=1")
        word = response.json()[0]  # Extract the word from the response
        return word

    def guess_letter(self, event=None):
        # Handle letter input from the player, check if the guess is correct, and update the game state
        guess = self.entry.get().lower()  # Get the input, convert to lowercase
        self.entry.delete(0, tk.END)  # Clear the input field

        # Validate the input: check if the guess is valid (1 character, not already guessed)
        if guess in self.guesses or len(guess) != 1:
            messagebox.showwarning("Invalid Input", "You have already guessed that letter or entered an invalid input!")
            return  # Exit if the input is invalid

        # Add the guessed letter to the list of guesses
        self.guesses += guess

        # If the guessed letter is not in the word, reduce the number of turns
        if guess not in self.word:
            self.turns -= 1  # Decrease the number of turns
            self.turns_label.config(text=f"Turns left: {self.turns}")  # Update the turns label

            # If no turns are left, the player loses the game
            if self.turns == 0:
                self.end_game(f"You Lose! The word was: {self.word}")
                return

        # Update the word display to show correctly guessed letters
        self.update_word_display()

        # If all letters are guessed, the player wins
        if "_" not in self.word_label.cget("text"):
            self.end_game(f"You Win! The word is: {self.word}")

    def update_word_display(self):
        # Update the label displaying the word with guessed letters and blanks for unguessed ones
        display_word = ""
        for char in self.word:  # Loop through each letter in the word
            if char in self.guesses:
                display_word += char + " "  # Show the guessed letter
            else:
                display_word += "_ "  # Show an underscore for unguessed letters
        self.word_label.config(text=display_word.strip())  # Update the label with the new word display

    def end_game(self, result_message):
        # Display a message indicating whether the player won or lost and disable the guess button
        messagebox.showinfo("Game Over", result_message)  # Show a messagebox with the result
        self.guess_button.config(state="disabled")  # Disable the guess button after the game ends
        self.reset_button.config(state="normal")  # Enable the reset button to restart the game

    def reset_game(self):
        # Reset the game state to start a new game
        self.word = self.get_random_word()  # Fetch a new word
        self.guesses = ''  # Clear previous guesses
        self.turns = 12  # Reset the number of turns
        self.turns_label.config(text=f"Turns left: {self.turns}")  # Update the turns label
        self.word_label.config(text="_ " * len(self.word))  # Reset the word display
        self.guess_button.config(state="normal")  # Re-enable the guess button
        self.reset_button.config(state="disabled")  # Disable the reset button until the game ends

# Main Program
if __name__ == "__main__":
    # Create the main window and start the game
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()  # Run the Tkinter event loop
