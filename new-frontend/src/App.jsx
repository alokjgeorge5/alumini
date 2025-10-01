import { BrowserRouter, Routes, Route, Navigate, Link } from 'react-router-dom'
import { useState, useEffect } from 'react'
import Home from './pages/Home'
import Mentorship from './pages/Mentorship'
import Opportunities from './pages/Opportunities'
import Stories from './pages/Stories'
import Login from './pages/Login'

function ProtectedApp() {
  const user = JSON.parse(localStorage.getItem('user') || '{}')
  
  return (
    <div style={{ fontFamily: 'system-ui, sans-serif', padding: 16 }}>
      <div style={{ marginBottom: 16, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span>Welcome, {user.name} ({user.role})</span>
        <button 
          onClick={() => { 
            localStorage.clear(); 
            window.location.reload(); 
          }}
          style={{
            padding: '8px 16px',
            backgroundColor: '#dc3545',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          Logout
        </button>
      </div>
      <nav style={{ display: 'flex', gap: 12, marginBottom: 16, borderBottom: '1px solid #eee', paddingBottom: 16 }}>
        <Link to="/" style={{ textDecoration: 'none', color: '#007bff', padding: '8px 12px', borderRadius: '4px' }}>Dashboard</Link>
        <Link to="/mentorship" style={{ textDecoration: 'none', color: '#007bff', padding: '8px 12px', borderRadius: '4px' }}>Mentorship</Link>
        <Link to="/opportunities" style={{ textDecoration: 'none', color: '#007bff', padding: '8px 12px', borderRadius: '4px' }}>Opportunities</Link>
        <Link to="/stories" style={{ textDecoration: 'none', color: '#007bff', padding: '8px 12px', borderRadius: '4px' }}>Stories</Link>
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

export default function App() {
  const [hasToken, setHasToken] = useState(!!localStorage.getItem('token'))

  if (!hasToken) {
    return (
      <BrowserRouter>
        <Routes>
          <Route path="*" element={<Login onLoginSuccess={() => setHasToken(true)} />} />
        </Routes>
      </BrowserRouter>
    )
  }

  return (
    <BrowserRouter>
      <ProtectedApp />
    </BrowserRouter>
  )
}
