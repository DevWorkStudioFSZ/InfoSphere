// components/DownloadForm.jsx
import { useState } from "react";

export default function DownloadForm({ defaultCity="", defaultCategory="" }) {
  const [city, setCity] = useState(defaultCity);
  const [category, setCategory] = useState(defaultCategory);
  const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:5000/api";

  async function downloadCSV() {
    try {
      const res = await fetch(`${API_URL}/download`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ city, category })
      });
      if (!res.ok) {
        const txt = await res.text();
        console.error("Download error:", txt);
        alert("Download failed: " + (txt || res.status));
        return;
      }

      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      const safeCity = city.replace(/\s+/g, "_") || "results";
      const safeCat = category.replace(/\s+/g, "_") || "data";
      a.download = `${safeCity}_${safeCat}.csv`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error(err);
      alert("Download failed (see console)");
    }
  }

  return (
    <div className="p-4 bg-white/5 rounded-lg">
      <div className="mb-2">
        <label className="block text-sm">City</label>
        <input value={city} onChange={e => setCity(e.target.value)} className="input-dark" placeholder="e.g. Karachi" />
      </div>
      <div className="mb-2">
        <label className="block text-sm">Category</label>
        <input value={category} onChange={e => setCategory(e.target.value)} className="input-dark" placeholder="e.g. library, restaurant, cafe" />
      </div>
      <div className="flex gap-2">
        <button className="btn-primary" onClick={downloadCSV}>Download CSV</button>
      </div>
    </div>
  );
}
