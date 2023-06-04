import axios from "axios"

export default async function keyExtractAPI(text: string, top_n: number) {
    const response = await axios.post("http://localhost:5000/keywords", {
        input: text,
        top_n: top_n
    });
    return response.data;
}