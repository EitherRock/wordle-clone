from pydantic import BaseModel

class GameSettings(BaseModel):
    word_length: int = 5
    max_tries: int = 5
    has_recurring_letters: bool = False
    allow_profanity: bool = False

default_settings = GameSettings()