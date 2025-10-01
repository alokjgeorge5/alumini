import { useEffect, useState } from 'react'

export default function Home() {
  const [status, setStatus] = useState('loading...')
  useEffect(() => {
    fetch('/api/health').then(async (r) => {
      const j = await r.json().catch(() => ({}))
      setStatus(r.ok ? `ok (db: ${j.db || 'ok'})` : 'degraded')
    }).catch(() => setStatus('offline'))
  }, [])
  return (
    <div>
      <h1>Alumni Connect</h1>
      <p>Backend health: {status}</p>
    </div>
  )
}


