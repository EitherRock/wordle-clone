import random
import os
from wordfreq import top_n_list
from termcolor import colored

import nltk
from nltk.corpus import stopwords, names
from nltk import pos_tag, word_tokenize

# Download NLTK resources
nltk.download('names')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('punkt')
nltk.download('punkt_tab')

stop_words = set(stopwords.words('english'))  # Get the stop words
word_list = top_n_list('en', 20000)  # Get top words

proper_noun_set = set(name.lower() for name in names.words())

def remove_proper_nouns(words):
    filtered = []
    for word in words:
        # Check if the word is in the proper noun set (lowercase names)
        if word.lower() in proper_noun_set:
            continue  # Skip the word if it's a proper noun

        # Tokenize and POS tag each word
        tokens = word_tokenize(word)
        tagged = pos_tag(tokens)
        
        # If no token is a proper noun (NNP or NNPS), keep the word
        if not any(tag == 'NNP' or tag == 'NNPS' for _, tag in tagged):
            filtered.append(word)
    
    return filtered


# Remove proper nouns
filtered_words = remove_proper_nouns(word_list)

# Remove stop words
filtered_words = [word for word in filtered_words if word.lower() not in stop_words and word.isalpha()]



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


def load_words(length, has_duplicates):
    # Filter word list for words that match the configured length
    filter = [word for word in filtered_words if len(word) == length and len(set(word)) == len(word)]

    # Include duplicate letters
    if has_duplicates:
        filter = [word for word in filtered_words if len(word) == length]
    
    return filter


if __name__ == '__main__':
    length, tries, has_duplicates = configure_game()

    # Load words of the configured length
    valid_words = load_words(length, has_duplicates)
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
