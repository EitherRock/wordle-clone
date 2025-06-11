
import React, { useEffect, useState } from "react";
import { fetchWord, WordResponse } from "../api/word";

const WordDisplay: React.FC = () => {
    const [word, setWord] = useState<WordResponse | null>(null);
    const [error, setError] = useState<string | null>(null);

    const getWord = async () => {
        try {
            const response = await fetchWord();
            setWord(response);
            setError(null);
        } catch (err) {
            console.error(err);
            setError("Failed to fetch a word.");
        }
    };

    useEffect(() => {
        getWord(); // Fetch once on mount
    }, []);

    return (
        <div>
            <p>Chosen Word: {word ? word.word : "Loading..."}</p>
            <button onClick={getWord}>Get New Word</button>
            {error && <p style={{ color: "red" }}>{error}</p>}
        </div>
    );
};

export default WordDisplay;
