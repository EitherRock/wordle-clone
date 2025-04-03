import nltk
from nltk.corpus import stopwords, names
from nltk import pos_tag, word_tokenize
from wordfreq import top_n_list
import random

# Download NLTK resources
nltk.download('names')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('punkt')
nltk.download('punkt_tab')

stop_words = set(stopwords.words('english'))
word_list = top_n_list('en', 30000)

proper_noun_set = set(name.lower() for name in names.words())

filtered_words_list = []

def remove_proper_nouns(words: list):
    filtered = []
    for word in words:
        # Check if the word is in the proper noun set
        if word.lower() in proper_noun_set:
            continue 

        # Tokenize and POS tag each word
        tokens = word_tokenize(word)
        tagged = pos_tag(tokens)
        
        if not any(tag == 'NNP' or tag == 'NNPS' for _, tag in tagged):
            filtered.append(word)
    
    return filtered

def process_words():
    global filtered_words_list

    # Remove proper nouns
    filtered_words = remove_proper_nouns(word_list)

    # Remove stop words
    filtered_words = [word for word in filtered_words if word.lower() not in stop_words and word.isalpha()]

    filtered_words_list = filtered_words

process_words()

def chosen_word(length: str, has_duplicates: bool):
    
    # Filter word list for words that match the configured length
    filter = [word for word in filtered_words_list if len(word) == length and len(set(word)) == len(word)]

    # Include duplicate letters
    if has_duplicates:
        filter = [word for word in filtered_words_list if len(word) == length]
    
    return random.choice(filter)