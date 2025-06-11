from typing import Union
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from util.filtered_words import chosen_word
from .settings import GameSettings, default_settings

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

current_settings = default_settings.model_copy()

@app.get('/settings', response_model=GameSettings)
def get_settings():
    return current_settings

@app.post('/settings', response_model=GameSettings)
def update_settings(updated_settings: GameSettings):
    global current_settings

    # add validattion
    current_settings = updated_settings
    return current_settings

@app.get('/')
def read_root():
    return {'Hello': 'World'}

@app.get('/word')
def random_word():

    word = chosen_word(
        current_settings.word_length, 
        current_settings.has_recurring_letters, 
        current_settings.allow_profanity
    )

    return {'word': word}



# create valid words list

# create model for game config

# create model for guess :str

# serve game config

# recieve updated game config

# serve random game word

# validate guess, check if entered word matches game word
