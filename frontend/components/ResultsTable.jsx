export default function ResultsTable({ results }) {
  return (
    <div className="overflow-x-auto rounded-lg shadow">
      <table className="min-w-full border border-gray-200">
        <thead className="bg-gray-100">
          <tr>
            <th className="px-4 py-2 text-left">Name</th>
            <th className="px-4 py-2 text-left">Address</th>
            <th className="px-4 py-2 text-left">Phone</th>
            <th className="px-4 py-2 text-left">Website</th>
            <th className="px-4 py-2 text-left">Rating</th>
            <th className="px-4 py-2 text-left">Rating Count</th>
            <th className="px-4 py-2 text-left">Category</th>
          </tr>
        </thead>
        <tbody>
          {results.map((item, i) => (
            <tr
              key={i}
              className="border-t hover:bg-gray-50 transition-colors"
            >
              <td className="px-4 py-2">{item.name || "N/A"}</td>
              <td className="px-4 py-2">{item.address || "N/A"}</td>
              <td className="px-4 py-2">{item.phone || "N/A"}</td>
              <td className="px-4 py-2">
                {item.website ? (
                  <a
                    href={item.website}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-600 underline"
                  >
                    Visit
                  </a>
                ) : (
                  "N/A"
                )}
              </td>
              <td className="px-4 py-2">{item.rating ?? "N/A"}</td>
              <td className="px-4 py-2">{item.rating_count ?? "N/A"}</td>
              <td className="px-4 py-2">{item.category || "N/A"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
