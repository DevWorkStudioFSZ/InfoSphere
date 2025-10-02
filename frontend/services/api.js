import axios from "axios";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function search(city, category, filters = {}) {
  try {
    const res = await axios.post(`${API_URL}/search`, {
      city,
      category,
      filters
    });
    return res.data.entities || []; // backend returns "entities"
  } catch (err) {
    console.error("API error in search:", err.response?.data || err.message);
    throw err;
  }
}
