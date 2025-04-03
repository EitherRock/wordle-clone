from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

from util.filtered_words import chosen_word 

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

@app.get('/')
def read_root():
    return {'Hello': 'World'}

@app.get('/items/{item_id}')
def read_item(item_id: int, q: Union[str, None] = None):
    return {'item_id': item_id, 'q': q}

@app.put('/items/{item_id}')
def update_item(item_id: int, item: Item):
    return {'item_name': item.name, 'item_id': item_id}

@app.get('/word')
def random_word():

    word = chosen_word(5, False)

    return {'word': word}


# create valid words list

# create model for game config

# create model for guess :str

# serve game config

# recieve updated game config

# serve random game word

# validate guess, check if entered word matches game word
