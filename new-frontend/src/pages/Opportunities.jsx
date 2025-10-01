import { useEffect, useState } from 'react'

export default function Opportunities() {
  const [items, setItems] = useState([])
  useEffect(() => {
    fetch('/api/opportunities/').then(r => r.json()).then(setItems).catch(() => setItems([]))
  }, [])
  return (
    <div>
      <h2>Opportunities</h2>
      <ul>
        {items.map(i => (<li key={i.id}>{i.company} — {i.role}</li>))}
      </ul>
    </div>
  )
}


