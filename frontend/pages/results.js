import { useRouter } from 'next/router'
import { useEffect, useState } from 'react'
import FilterPanel from '../components/FilterPanel'
import ResultsTable from '../components/ResultsTable'
import MapView from '../components/MapView'
import { search } from '../services/api'

export default function ResultsPage() {
  const router = useRouter()
  const { city, category } = router.query
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [filters, setFilters] = useState({ minRating: 0, openNow: false })

  useEffect(() => {
    if (!city || !category) return
    setLoading(true)
    search(city, category, filters)
      .then((data) => setResults(data))
      .catch((err) => {
        console.error(err)
        setResults([])
      })
      .finally(() => setLoading(false))
  }, [city, category, filters])

  return (
    <div className="min-h-screen p-6 bg-gray-50">
      <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <div className="bg-white p-4 rounded shadow">
            <h2 className="text-xl font-semibold">Results — {city} / {category}</h2>
            <FilterPanel filters={filters} setFilters={setFilters} />
            {loading ? (
              <div className="py-10 text-center">Loading...</div>
            ) : (
              <ResultsTable data={results} />
            )}
          </div>
        </div>

        <div>
          <div className="bg-white p-4 rounded shadow">
            <h3 className="font-semibold mb-2">Map View</h3>
            <MapView points={results} />
          </div>
        </div>
      </div>
    </div>
  )
}

