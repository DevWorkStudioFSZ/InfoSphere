import { useRouter } from "next/router";
import { useEffect, useState } from "react";
import { search } from "../services/api";
import ResultsTable from "../components/ResultsTable";
import MapView from "../components/MapView";

export default function ResultsPage() {
  const router = useRouter();
  const { city, category } = router.query;
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (city && category) {
      setLoading(true);
      search(city, category)
        .then((data) => {
          setResults(data);
          setError(null);
        })
        .catch(() => {
          setError("⚠️ Failed to fetch results. Please try again.");
          setResults([]);
        })
        .finally(() => {
          setLoading(false);
        });
    }
  }, [city, category]);

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold">
        Results for <span className="text-blue-600">{city}</span> –{" "}
        <span className="text-green-600">{category}</span>
      </h1>

      {loading && <p className="text-gray-500">Loading...</p>}
      {error && <p className="text-red-500">{error}</p>}

      {!loading && !error && results.length === 0 && (
        <p className="text-gray-500">No results found.</p>
      )}

      {!loading && results.length > 0 && (
        <>
          <ResultsTable results={results} />
          <div className="h-[500px]">
            <MapView results={results} />
          </div>
        </>
      )}
    </div>
  );
}
