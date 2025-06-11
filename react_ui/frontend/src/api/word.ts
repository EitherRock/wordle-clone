import axios from 'axios';

export interface WordResponse {
    word: string;
}

export const fetchWord = async (): Promise<WordResponse> => {
    try {
        const response = await axios.get<WordResponse>('http://localhost:8000/word')
        return response.data;
    } catch (error) {
        console.error(error)
        throw error;
    }
};