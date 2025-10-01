import { useEffect, useState } from 'react'

export default function Stories() {
  const [items, setItems] = useState([])
  useEffect(() => {
    fetch('/api/stories/').then(r => r.json()).then(setItems).catch(() => setItems([]))
  }, [])
  return (
    <div>
      <h2>Success Stories</h2>
      <ul>
        {items.map(i => (<li key={i.id}>{i.title} — {i.author}</li>))}
      </ul>
    </div>
  )
}


