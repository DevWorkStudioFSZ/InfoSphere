import '../styles/globals.css'
import 'leaflet/dist/leaflet.css'   // ✅ Add this

export default function MyApp({ Component, pageProps }) {
  return <Component {...pageProps} />
}

