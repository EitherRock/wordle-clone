import json
import random
import os
from termcolor import colored

import nltk

nltk.download('words')
from nltk.corpus import words

word_list = words.words()


# Define a function to set up game configuration
def configure_game():
    print("Welcome to Wordle Clone!")
    while True:
        try:
            length = int(input("Enter word length: "))
            tries = int(input("Enter number of tries: "))
            return length, tries
        except ValueError:
            print("Please enter a valid number.")


def load_words():
    # Filter word list for words that match the specified length
    return [word for word in word_list if word.isalpha() and len(set(word)) == len(word)]


if __name__ == '__main__':
    length, tries = configure_game()  # Initialize game with user inputs

    # Load words of the specified length
    valid_words = [word for word in load_words() if len(word) == length]
    chosen_word = random.choice(valid_words)
    letter_list = list(chosen_word)  # Convert chosen word into a list of letters

    tries_list = [['_' for _ in range(length)] for _ in range(tries)]
    try_counter = 0

    while try_counter < tries:
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen for each attempt

        # Display current guesses and progress
        for tri in tries_list:
            print(*tri, sep='')
        print("\n")

        guess_input = input(f"Attempt {try_counter + 1}/{tries}: Guess the word: ")

        if guess_input == 'quit':
            print("Game aborted.")
            break

        if len(guess_input) != length:
            print(f"Please enter a word of length {length}.")
            continue

        # Process the guess
        for g_letter in range(len(guess_input)):
            if guess_input[g_letter] == letter_list[g_letter]:
                tries_list[try_counter][g_letter] = colored(f'{guess_input[g_letter]}', 'green')
            elif guess_input[g_letter] in letter_list:
                tries_list[try_counter][g_letter] = colored(f'{guess_input[g_letter]}', 'magenta')
            else:
                tries_list[try_counter][g_letter] = colored(f'{guess_input[g_letter]}', 'grey')

        # Check for a win
        if guess_input == chosen_word:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Congratulations, you guessed the word!")
            break

        try_counter += 1

    if try_counter == tries:
        print(f"Game over! The correct word was '{chosen_word}'.")
