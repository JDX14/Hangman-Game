import random
import requests

def play_game():
    # Fetch a random word from an API
    response = requests.get("https://random-word-api.herokuapp.com/word?number=1")
    word = response.json()[0]
   
    print("Guess the characters")

    guesses = ''
    turns = 12

    while turns > 0:
        failed = 0

        for char in word:
            if char in guesses:
                print(char, end=" ")
            else:
                print("_", end=" ")
                failed += 1

        if failed == 0:
            print("\nYou Win!")
            print("The word is:", word)
            break

        print()
        guess = input("Guess a character: ")

        guesses += guess

        if guess not in word:
            turns -= 1
            print("Wrong!")
            print(f"You have {turns} more guesses")

            if turns == 0:
                print("You Lose!")
                print(f"The word was: {word}")  # Revealing the word here

# Main loop to restart the game
while True:
    play_game()
    play_again = input("Do you want to play again? (y/n): ").lower()
    if play_again != 'y':
        print("Thank you for playing!")
        break