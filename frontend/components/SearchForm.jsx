import { useState } from 'react'

const CATEGORIES = [
  { value: 'libraries', label: 'Libraries' },
  { value: 'tuition', label: 'Tuition Centers' },
  { value: 'restaurants', label: 'Restaurants' },
  { value: 'coffee', label: 'Coffee Shops' }
]

export default function SearchForm({ onSearch }) {
  const [city, setCity] = useState('')
  const [category, setCategory] = useState(CATEGORIES[0].value)

  const submit = (e) => {
    e.preventDefault()
    if (!city || !city.trim()) {
      alert("Please enter a city name")
      return
    }
    onSearch({ city: city.trim(), category })
  }

  return (
    <form onSubmit={submit} className="space-y-4">
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <input
          type="text"
          placeholder="Enter city (e.g. Lahore)"
          className="border border-gray-300 p-2 rounded w-full text-black focus:outline-none focus:ring-2 focus:ring-blue-300"
          value={city}
          onChange={(e) => setCity(e.target.value)}
        />

        <select
          className="border border-gray-300 p-2 rounded w-full text-black focus:outline-none focus:ring-2 focus:ring-blue-300"
          value={category}
          onChange={(e) => setCategory(e.target.value)}
        >
          {CATEGORIES.map((c) => (
            <option key={c.value} value={c.value}>
              {c.label}
            </option>
          ))}
        </select>
      </div>

      <div className="flex items-center gap-3">
        <button
          type="submit"
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded shadow"
        >
          Search
        </button>

        <button
          type="button"
          onClick={() => {
            setCity('')
            setCategory(CATEGORIES[0].value)
          }}
          className="bg-gray-200 hover:bg-gray-300 text-black px-4 py-2 rounded shadow"
        >
          Reset
        </button>
      </div>
    </form>
  )
}
