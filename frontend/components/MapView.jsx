// "use client";

// import dynamic from "next/dynamic";
// import { useEffect, useState } from "react";

// // Dynamically import react-leaflet components (disable SSR)
// const MapContainer = dynamic(() => import("react-leaflet").then(mod => mod.MapContainer), { ssr: false });
// const TileLayer = dynamic(() => import("react-leaflet").then(mod => mod.TileLayer), { ssr: false });
// const Marker = dynamic(() => import("react-leaflet").then(mod => mod.Marker), { ssr: false });
// const Popup = dynamic(() => import("react-leaflet").then(mod => mod.Popup), { ssr: false });

// export default function MapView({ results }) {
//   const [L, setL] = useState(null);
//   const [markerIcon, setMarkerIcon] = useState(null);

//   useEffect(() => {
//     // Import leaflet only in the browser
//     import("leaflet").then((leaflet) => {
//       setL(leaflet);
//       setMarkerIcon(
//         new leaflet.Icon({
//           iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
//           iconSize: [25, 41],
//           iconAnchor: [12, 41],
//         })
//       );
//     });
//   }, []);

//   if (!results || results.length === 0) {
//     return <p className="text-gray-500">No map data available</p>;
//   }

//   if (!L || !markerIcon) {
//     return <p className="text-gray-400">Loading map...</p>; // Wait until leaflet loads
//   }

//   const first = results[0].location || { lat: 31.5497, lng: 74.3436 }; // fallback: Lahore

//   return (
//     <MapContainer
//       center={[first.lat, first.lng]}
//       zoom={12}
//       style={{ height: "100%", width: "100%" }}
//       className="rounded-lg shadow"
//     >
//       <TileLayer
//         url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
//         attribution="&copy; OpenStreetMap contributors"
//       />
//       {results
//         .filter((r) => r.location)
//         .map((r, i) => (
//           <Marker
//             key={i}
//             position={[r.location.lat, r.location.lng]}
//             icon={markerIcon}
//           >
//             <Popup>
//               <strong>{r.name}</strong>
//               <br />
//               {r.address}
//               <br />
//               Rating: {r.rating ?? "N/A"}
//             </Popup>
//           </Marker>
//         ))}
//     </MapContainer>
//   );
// }


// mapview.jsx
"use client";

import "leaflet/dist/leaflet.css";
import dynamic from "next/dynamic";
import { useEffect, useMemo, useState } from "react";

// Dynamically import react-leaflet components (disable SSR)
const MapContainer = dynamic(() => import("react-leaflet").then((mod) => mod.MapContainer), { ssr: false });
const TileLayer = dynamic(() => import("react-leaflet").then((mod) => mod.TileLayer), { ssr: false });
const Marker = dynamic(() => import("react-leaflet").then((mod) => mod.Marker), { ssr: false });
const Popup = dynamic(() => import("react-leaflet").then((mod) => mod.Popup), { ssr: false });

export default function MapView({ results }) {
  const [L, setL] = useState(null);
  const [markerIcon, setMarkerIcon] = useState(null);

  useEffect(() => {
    // Import leaflet only in the browser and create icon once
    import("leaflet").then((leaflet) => {
      setL(leaflet);
      const icon = new leaflet.Icon({
        // explicit icon URL avoids webpack/asset path issues
        iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
        iconRetinaUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
        shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41],
      });
      setMarkerIcon(icon);
    });
  }, []);

  // Helper: normalize/interpret coordinates from many formats
  const extractLatLng = (r) => {
    if (!r) return null;

    // 1) location object {lat, lng}
    if (r.location && r.location.lat != null && r.location.lng != null) {
      const lat = Number(r.location.lat);
      const lng = Number(r.location.lng);
      if (Number.isFinite(lat) && Number.isFinite(lng)) return { lat, lng };
    }

    // 2) lat & lng
    if (r.lat != null && r.lng != null) {
      const lat = Number(r.lat);
      const lng = Number(r.lng);
      if (Number.isFinite(lat) && Number.isFinite(lng)) return { lat, lng };
    }

    // 3) lat & lon
    if (r.lat != null && r.lon != null) {
      const lat = Number(r.lat);
      const lng = Number(r.lon);
      if (Number.isFinite(lat) && Number.isFinite(lng)) return { lat, lng };
    }

    // 4) latitude & longitude
    if (r.latitude != null && r.longitude != null) {
      const lat = Number(r.latitude);
      const lng = Number(r.longitude);
      if (Number.isFinite(lat) && Number.isFinite(lng)) return { lat, lng };
    }

    // 5) geometry.coordinates or coordinates array (could be [lon, lat] or [lat, lon])
    const coords = r.coordinates || (r.geometry && r.geometry.coordinates);
    if (Array.isArray(coords) && coords.length >= 2) {
      const a = Number(coords[0]);
      const b = Number(coords[1]);
      if (Number.isFinite(a) && Number.isFinite(b)) {
        // If first value is valid lat range (-90..90) and second fits lon (-180..180) => [lat, lon]
        if (a >= -90 && a <= 90 && b >= -180 && b <= 180) return { lat: a, lng: b };
        // If first looks like lon and second looks like lat (GeoJSON) => [lon, lat]
        if (a >= -180 && a <= 180 && b >= -90 && b <= 90) return { lat: b, lng: a };
      }
    }

    // no usable coords
    return null;
  };

  const points = useMemo(() => {
    if (!Array.isArray(results)) return [];
    const arr = results
      .map((r) => {
        const ll = extractLatLng(r);
        if (!ll) return null;
        return {
          name: r.name || r.title || "Unknown",
          address: r.address || r.tags?.addr_full || r.tags?.addr_street || "",
          rating: r.rating ?? r.rating_average ?? null,
          lat: ll.lat,
          lng: ll.lng,
        };
      })
      .filter(Boolean);
    // debugging helpful line — remove or comment out if not needed
    // console.log("Map points:", arr);
    return arr;
  }, [results]);

  if (!results || results.length === 0) {
    return <p className="text-gray-500">No map data available</p>;
  }

  if (!L || !markerIcon) {
    return <p className="text-gray-400">Loading map...</p>;
  }

  if (points.length === 0) {
    return <p className="text-gray-500">No geolocation data found for results.</p>;
  }

  const first = points[0];

  return (
    <MapContainer
      center={[first.lat, first.lng]}
      zoom={12}
      style={{ height: "100%", width: "100%" }}
      className="rounded-lg shadow"
      scrollWheelZoom={true}
    >
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution="&copy; OpenStreetMap contributors"
      />

      {points.map((p, i) => (
        <Marker key={i} position={[p.lat, p.lng]} icon={markerIcon}>
          <Popup>
            <strong>{p.name}</strong>
            <br />
            {p.address}
            <br />
            Rating: {p.rating ?? "N/A"}
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
}
