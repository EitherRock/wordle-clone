import os
from termcolor import colored
from util.filtered_words import chosen_word


def configure_game():
    print("Welcome to Wordle Clone!")
    while True:
        try:
            length = int(input("Enter word length: "))
            tries = int(input("Enter number of tries: "))
            duplicates_input = input("Include duplicate letters? (true/false): ").strip().lower()
            
            if duplicates_input == 'true':
                has_duplicates = True
            elif duplicates_input == 'false':
                has_duplicates = False
            else:
                raise ValueError
            
            return length, tries, has_duplicates
        except ValueError:
            print("Please enter a valid value.")


if __name__ == '__main__':
    length, tries, has_duplicates = configure_game()

    word = chosen_word(length, has_duplicates)
    letter_list = list(word)  # Convert chosen word into a list of letters

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
        if guess_input == word:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Congratulations, you guessed the word!")
            break

        try_counter += 1

    if try_counter == tries:
        print(f"Game over! The correct word was '{word}'.")
