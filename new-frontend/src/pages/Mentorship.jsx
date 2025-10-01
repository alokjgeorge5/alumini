import { useEffect, useState } from 'react'

export default function Mentorship() {
  const [items, setItems] = useState([])
  useEffect(() => {
    fetch('/api/mentorship/').then(r => r.json()).then(setItems).catch(() => setItems([]))
  }, [])
  return (
    <div>
      <h2>Mentorship</h2>
      <ul>
        {items.map(i => (<li key={i.id}>{i.title} — {i.mentor}</li>))}
      </ul>
    </div>
  )
}


