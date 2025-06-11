import axios from 'axios';

export interface GameSettings {
    word_length: number;
    max_tries: number;
    has_recurring_letters: boolean;
    allow_profanity: boolean;
}

export const fetchSettings = async (): Promise<GameSettings> => {
    const response = await axios.get('http://localhost:8000/settings');
    const data = response.data;
    
    return {
        word_length: data.word_length ?? 5,
        max_tries: data.max_tries ?? 5,
        has_recurring_letters: data.has_recurring_letters ?? false,
        allow_profanity: data.allow_profanity ?? false,
    }; 
};

export const updateSettings = async (settings: GameSettings) => {
    const response = await axios.post('http://localhost:8000/settings', settings);

    return response.data;
}