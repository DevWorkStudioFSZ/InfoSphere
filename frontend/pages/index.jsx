// import { useState } from "react";
// import { useRouter } from "next/router";

// const CATEGORIES = [
//   "Restaurants",
//   "Libraries",
//   "Cafes",
//   "Tuition Centers",
//   "Hospitals",
//   "Schools",
//   "Shopping",
//   "Parks",
// ];

// export default function Home() {
//   const router = useRouter();
//   const [city, setCity] = useState("");
//   const [category, setCategory] = useState("");

//   const handleSearch = (e) => {
//     e.preventDefault();
//     if (!city.trim() || !category.trim()) {
//       alert("Please enter a city AND select a category.");
//       return;
//     }
//     router.push(
//       `/results?city=${encodeURIComponent(city)}&category=${encodeURIComponent(
//         category
//       )}`
//     );
//   };

//   const handleReset = () => {
//     setCity("");
//     setCategory("");
//   };

//   return (
//     <div className="min-h-screen flex flex-col bg-[color:var(--background)]">
//       {/* Hero Section */}
//       <div className="flex-1 flex flex-col items-center justify-center text-center px-6 py-24">
//         <h1 className="text-5xl font-extrabold text-[color:var(--button-primary)] mb-4">
//           Discover Places Around You
//         </h1>
//         <p className="text-lg text-gray-300 mb-8 max-w-2xl">
//           Search for restaurants, parks, hospitals, libraries & more across cities.
//         </p>

//         <div className="w-full max-w-xl">
//           <form onSubmit={handleSearch} className="grid grid-cols-1 sm:grid-cols-2 gap-4">
//             <input
//               type="text"
//               placeholder="Enter city (e.g. Lahore)"
//               value={city}
//               onChange={(e) => setCity(e.target.value)}
//               className="input-dark"
//             />
//             <select
//               value={category}
//               onChange={(e) => setCategory(e.target.value)}
//               className="input-dark"
//             >
//               <option value="">Select category</option>
//               {CATEGORIES.map((cat) => (
//                 <option key={cat} value={cat.toLowerCase()}>
//                   {cat}
//                 </option>
//               ))}
//             </select>
//             <button
//               type="submit"
//               className="btn-primary col-span-1 sm:col-span-2"
//             >
//               🔍 Search
//             </button>
//             <button
//               type="button"
//               onClick={handleReset}
//               className="btn-secondary col-span-1 sm:col-span-2"
//             >
//               Reset
//             </button>
//           </form>
//         </div>
//       </div>

//       {/* Features Section */}
//       <div className="py-12 bg-[color:var(--card-bg)] text-center">
//         <h2 className="text-3xl font-bold text-[color:var(--foreground)] mb-6">Why InfoSphere?</h2>
//         <div className="max-w-4xl mx-auto grid grid-cols-1 sm:grid-cols-3 gap-8 px-4">
//           <Feature title="Accurate Search" description="Find places in city by category and filters." />
//           <Feature title="Fast Results" description="Powered by fast backend & live API data." />
//           <Feature title="Easy to Use" description="Simple design, minimal steps." />
//         </div>
//       </div>

//       {/* Call to Action */}
//       <div className="py-16 text-center">
//         <button
//           className="btn-primary px-8 py-4 text-xl mx-auto"
//           onClick={handleSearch}
//         >
//           Start Searching →
//         </button>
//       </div>
//     </div>
//   );
// }

// function Feature({ title, description }) {
//   return (
//     <div className="bg-[color:var(--background)] border border-[color:var(--input-border)] rounded-lg p-6 shadow-lg mx-4">
//       <h3 className="text-2xl font-semibold text-[color:var(--foreground)] mb-2">{title}</h3>
//       <p className="text-gray-400">{description}</p>
//     </div>
//   );
// }



import { useState } from "react";
import { useRouter } from "next/router";

const CATEGORIES = [
  "Restaurants",
  "Libraries",
  "Cafes",
  "Tuition Centers",
  "Hospitals",
  "Schools",
  "Shopping",
  "Parks",
];

export default function Home() {
  const router = useRouter();
  const [city, setCity] = useState("");
  const [category, setCategory] = useState("");

  const handleSearch = (e) => {
    e.preventDefault();
    if (!city.trim() || !category.trim()) {
      alert("Please enter a city AND select a category.");
      return;
    }
    router.push(
      `/results?city=${encodeURIComponent(city)}&category=${encodeURIComponent(
        category
      )}`
    );
  };

  const handleReset = () => {
    setCity("");
    setCategory("");
  };

  return (
    <div className="min-h-screen flex flex-col bg-[color:var(--background)]">
      {/* 🌐 Navbar */}
      <nav className="flex justify-between items-center px-8 py-4 bg-[color:var(--card-bg)] shadow-lg sticky top-0 z-50">
        <h1 className="text-2xl font-bold text-[color:var(--button-primary)]">
          InfoSphere
        </h1>
        <div className="space-x-6 text-gray-300">
          <a href="/" className="hover:text-[color:var(--button-primary)]">Home</a>
          <a href="#features" className="hover:text-[color:var(--button-primary)]">Features</a>
          <a href="#about" className="hover:text-[color:var(--button-primary)]">About</a>
        </div>
      </nav>

      {/* 🎯 Hero Section */}
      <div className="flex-1 flex flex-col items-center justify-center text-center px-6 py-24 bg-gradient-to-b from-[#0f172a] to-[#1e293b]">
        <h1 className="text-6xl font-extrabold text-[color:var(--button-primary)] mb-4">
          Discover Places Around You
        </h1>
        <p className="text-lg text-gray-300 mb-8 max-w-2xl">
          Find the best restaurants, parks, libraries, hospitals & more in your city instantly.
        </p>

        <div className="w-full max-w-xl">
          <form onSubmit={handleSearch} className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <input
              type="text"
              placeholder="Enter city (e.g. Lahore)"
              value={city}
              onChange={(e) => setCity(e.target.value)}
              className="input-dark"
            />
            <select
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              className="input-dark"
            >
              <option value="">Select category</option>
              {CATEGORIES.map((cat) => (
                <option key={cat} value={cat.toLowerCase()}>
                  {cat}
                </option>
              ))}
            </select>
            <button type="submit" className="btn-primary col-span-1 sm:col-span-2">
              🔍 Search
            </button>
            <button
              type="button"
              onClick={handleReset}
              className="btn-secondary col-span-1 sm:col-span-2"
            >
              Reset
            </button>
          </form>
        </div>
      </div>

      {/* ⭐ Features Section */}
      <div id="features" className="py-12 bg-[color:var(--card-bg)] text-center">
        <h2 className="text-3xl font-bold text-[color:var(--foreground)] mb-6">Why InfoSphere?</h2>
        <div className="max-w-4xl mx-auto grid grid-cols-1 sm:grid-cols-3 gap-8 px-4">
          <Feature title="Accurate Search" description="Find places in city by category and filters." />
          <Feature title="Fast Results" description="Powered by fast backend & live API data." />
          <Feature title="Easy to Use" description="Simple design, minimal steps." />
        </div>
      </div>

      {/* 📢 Call to Action */}
      <div id="about" className="py-16 text-center">
        <button
          className="btn-primary px-8 py-4 text-xl mx-auto"
          onClick={handleSearch}
        >
          Start Searching →
        </button>
      </div>
    </div>
  );
}

function Feature({ title, description }) {
  return (
    <div className="bg-[color:var(--background)] border border-[color:var(--input-border)] rounded-lg p-6 shadow-lg mx-4">
      <h3 className="text-2xl font-semibold text-[color:var(--foreground)] mb-2">{title}</h3>
      <p className="text-gray-400">{description}</p>
    </div>
  );
}
