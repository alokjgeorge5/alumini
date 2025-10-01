import { useEffect, useState } from 'react'

export default function Opportunities() {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState('all')
  const user = JSON.parse(localStorage.getItem('user') || '{}')

  useEffect(() => {
    fetch('/api/opportunities')
      .then(r => r.json())
      .then(setItems)
      .catch(() => setItems([]))
      .finally(() => setLoading(false))
  }, [])

  const filteredItems = items.filter(item => {
    if (filter === 'all') return true
    return item.type === filter
  })

  const handleApply = async (opportunityId) => {
    if (user.role !== 'student') {
      alert('Only students can apply for opportunities')
      return
    }

    try {
      const token = localStorage.getItem('token')
      const response = await fetch('/api/applications', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          opportunity_id: opportunityId,
          opportunity_type: 'job',
          cover_letter: 'I am interested in this opportunity and would like to apply.'
        })
      })

      if (response.ok) {
        alert('Application submitted successfully!')
      } else {
        const error = await response.json()
        alert('Error: ' + (error.error || 'Failed to submit application'))
      }
    } catch (err) {
      alert('Error submitting application: ' + err.message)
    }
  }

  if (loading) {
    return <div style={{ textAlign: 'center', padding: '50px' }}>Loading opportunities...</div>
  }

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h2>Job & Internship Opportunities</h2>
        <div>
          <label style={{ marginRight: '10px' }}>Filter:</label>
          <select 
            value={filter} 
            onChange={(e) => setFilter(e.target.value)}
            style={{ padding: '5px 10px', borderRadius: '4px', border: '1px solid #ccc' }}
          >
            <option value="all">All</option>
            <option value="full-time">Full-time</option>
            <option value="part-time">Part-time</option>
            <option value="internship">Internship</option>
            <option value="contract">Contract</option>
          </select>
        </div>
      </div>

      <div style={{ display: 'grid', gap: '20px' }}>
        {filteredItems.length > 0 ? (
          filteredItems.map(item => (
            <div key={item.id} style={{ 
              padding: '20px', 
              border: '1px solid #ddd', 
              borderRadius: '8px', 
              backgroundColor: '#f8f9fa' 
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <div style={{ flex: 1 }}>
                  <h3 style={{ margin: '0 0 10px 0', color: '#007bff' }}>{item.title}</h3>
                  <p style={{ margin: '5px 0', fontSize: '18px', fontWeight: 'bold' }}>{item.company}</p>
                  <p style={{ margin: '5px 0', color: '#666' }}>
                    <strong>Type:</strong> {item.type} | 
                    <strong> Location:</strong> {item.location} | 
                    <strong> Posted:</strong> {new Date(item.created_at).toLocaleDateString()}
                  </p>
                  <p style={{ margin: '10px 0' }}>{item.description}</p>
                  <div style={{ marginTop: '15px' }}>
                    <strong>Requirements:</strong>
                    <ul style={{ margin: '5px 0', paddingLeft: '20px' }}>
                      {item.requirements?.split(',').map((req, idx) => (
                        <li key={idx}>{req.trim()}</li>
                      ))}
                    </ul>
                  </div>
                </div>
                <div style={{ marginLeft: '20px', textAlign: 'right' }}>
                  <div style={{ 
                    padding: '5px 10px', 
                    backgroundColor: '#28a745', 
                    color: 'white', 
                    borderRadius: '4px',
                    marginBottom: '10px',
                    fontSize: '14px'
                  }}>
                    {item.type}
                  </div>
                  {user.role === 'student' && (
                    <button 
                      onClick={() => handleApply(item.id)}
                      style={{
                        padding: '10px 20px',
                        backgroundColor: '#007bff',
                        color: 'white',
                        border: 'none',
                        borderRadius: '4px',
                        cursor: 'pointer',
                        fontSize: '14px'
                      }}
                    >
                      Apply Now
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))
        ) : (
          <div style={{ textAlign: 'center', padding: '50px', color: '#666' }}>
            No opportunities found for the selected filter.
          </div>
        )}
      </div>
    </div>
  )
}


