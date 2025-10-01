import { Link, Route, Routes } from 'react-router-dom'
import Home from './pages/Home'
import Mentorship from './pages/Mentorship'
import Opportunities from './pages/Opportunities'
import Stories from './pages/Stories'

export default function App() {
  return (
    <div style={{ fontFamily: 'system-ui, sans-serif', padding: 16 }}>
      <nav style={{ display: 'flex', gap: 12, marginBottom: 16 }}>
        <Link to="/">Dashboard</Link>
        <Link to="/mentorship">Mentorship</Link>
        <Link to="/opportunities">Opportunities</Link>
        <Link to="/stories">Stories</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/mentorship" element={<Mentorship />} />
        <Route path="/opportunities" element={<Opportunities />} />
        <Route path="/stories" element={<Stories />} />
      </Routes>
    </div>
  )
}


