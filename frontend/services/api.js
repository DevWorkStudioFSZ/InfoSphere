import axios from 'axios'

const USE_MOCK = process.env.NEXT_PUBLIC_USE_MOCK === 'true'
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000'

export async function search(city, category, filters = {}) {
  if (USE_MOCK) {
    const mod = await import('../utils/mockData')
    let data = mod.mockResults.filter(r => r.city.toLowerCase() === city.toLowerCase())
    if (filters.minRating) data = data.filter(r => (r.rating_average ?? 0) >= filters.minRating)
    if (filters.openNow) data = data.filter(r => r.open_now)
    return data
  } else {
    const res = await axios.get(`${API_URL}/search`, {
      params: { city, category, ...filters }
    })
    return res.data.entities ?? []
  }
}
