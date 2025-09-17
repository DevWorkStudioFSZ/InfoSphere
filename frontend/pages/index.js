import { useRouter } from 'next/router'
import SearchForm from '../components/SearchForm'

export default function Home() {
  const router = useRouter()

  const onSearch = ({ city, category }) => {
    router.push({
      pathname: '/results',
      query: { city, category }
    })
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-4xl mx-auto bg-white p-6 rounded shadow">
        <h1 className="text-2xl font-semibold mb-4">Pakistan City Data Extractor</h1>
        <SearchForm onSearch={onSearch} />
      </div>
    </div>
  )
}
