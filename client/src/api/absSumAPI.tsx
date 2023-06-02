import axios from "axios";

export default async function absSumAPI(text: string) {
    const response = await axios.post("http://localhost:5000/summarize", {
        input: text,
    });
    return response.data;
}