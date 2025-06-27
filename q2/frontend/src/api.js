import axios from 'axios';

const API_URL = 'http://localhost:8000';

export const analyzeImage = async (image, question) => {
    const formData = new FormData();
    formData.append('image', image);
    formData.append('question', question);

    try {
        const response = await axios.post(`${API_URL}/analyze`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data;
    } catch (error) {
        throw new Error(error.response?.data?.detail || 'Failed to analyze image');
    }
}; 