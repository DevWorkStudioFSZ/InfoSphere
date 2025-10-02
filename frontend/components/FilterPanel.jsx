export default function FilterPanel({ filters, setFilters }) {
  const update = (k, v) => setFilters(prev => ({ ...prev, [k]: v }))

  return (
    <div className="my-4 p-3 bg-gray-50 rounded border border-gray-100 flex flex-wrap gap-4 items-center">
      <label className="flex items-center gap-2 text-sm text-gray-700">
        Min rating:
        <select
          value={filters.minRating}
          onChange={e => update('minRating', Number(e.target.value))}
          className="border border-gray-300 p-1 rounded ml-2"
        >
          <option value={0}>Any</option>
          <option value={3}>3+</option>
          <option value={4}>4+</option>
        </select>
      </label>

      <label className="flex items-center gap-2 text-sm text-gray-700">
        <input
          type="checkbox"
          className="w-4 h-4"
          checked={filters.openNow}
          onChange={e => update('openNow', e.target.checked)}
        />
        Open now
      </label>
    </div>
  )
}
