import React, { useEffect, useState } from "react";
import { GameSettings, fetchSettings, updateSettings } from "../api/settings";
import { fetchWord, WordResponse } from "../api/word";


const SettingsForm: React.FC = () => {
    const [chosenWord, setChosenWord] = useState<WordResponse>({word:""});

    const [settings, setSettings] = useState<GameSettings>({
        word_length: 5,
        max_tries: 5,
        has_recurring_letters: false,
        allow_profanity: false,
    });

    const [error, setError] = useState<string | null>();

    useEffect(() => {
        console.log("Fetching settings and word...");

        const loadData = async () => {
            try {
                const settings = await fetchSettings();
                setSettings(settings);
            } catch (err) {
                setError('Failed to set setting. Please try again')
            }
            
            
            try {
                const word = await fetchWord();
                setChosenWord(word)
            } catch (err) {
                setError('Failed to generate chosen word. Please try again.')
            }
        };
        loadData();
    }, []);


    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, type, value, checked } = e.target;
        setSettings({
            ...settings,
            [name]: type === 'checkbox' ? checked : Number(value),
        });


    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        await updateSettings(settings);
        alert('Settings saved!');
    };

    return (
        
        <form onSubmit={handleSubmit}>
            {error && <p style={{ color: 'red' }}>{error}</p>}

            <label>
                Word Length:
                <input name="word_length" type="number" value={settings.word_length} onChange={handleChange} />
            </label>
            <br />
            <label>
                Max Tries:
                <input name="max_tries" type="number" value={settings.max_tries} onChange={handleChange} />
            </label>
            <br />
            <label>
                Allow Recurring Letters:
                <input name="has_recurring_letters" type="checkbox" checked={settings.has_recurring_letters} onChange={handleChange} />
            </label>
            <br />
            <label>
                Allow Profanity:
                <input name="allow_profanity" type="checkbox" checked={settings.allow_profanity} onChange={handleChange} />
            </label>
            <br />
            <p>{chosenWord ? chosenWord.word : "Loading word..."}</p>
            <button type="submit">Save Settings</button>
        </form>
    );
}

export default SettingsForm