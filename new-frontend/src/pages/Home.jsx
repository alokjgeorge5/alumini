import { useEffect, useState } from 'react'

export default function Home() {
  const [status, setStatus] = useState('loading...')
  const [stats, setStats] = useState({})
  const [recentOpportunities, setRecentOpportunities] = useState([])
  const [recentStories, setRecentStories] = useState([])
  const user = JSON.parse(localStorage.getItem('user') || '{}')

  useEffect(() => {
    // Check backend health
    fetch('/api/health').then(async (r) => {
      const j = await r.json().catch(() => ({}))
      setStatus(r.ok ? `ok (db: ${j.db || 'ok'})` : 'degraded')
    }).catch(() => setStatus('offline'))

    // Load dashboard data
    Promise.all([
      fetch('/api/opportunities').then(r => r.json()).catch(() => []),
      fetch('/api/stories').then(r => r.json()).catch(() => [])
    ]).then(([opportunities, stories]) => {
      setRecentOpportunities(opportunities.slice(0, 3))
      setRecentStories(stories.slice(0, 3))
      setStats({
        opportunities: opportunities.length,
        stories: stories.length
      })
    })
  }, [])

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
      <h1>Alumni Connect Dashboard</h1>
      <p style={{ color: status === 'ok (db: ok)' ? 'green' : 'red' }}>
        Backend health: {status}
      </p>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '20px', marginTop: '20px' }}>
        {/* Stats Cards */}
        <div style={{ padding: '20px', border: '1px solid #ddd', borderRadius: '8px', backgroundColor: '#f8f9fa' }}>
          <h3>Platform Statistics</h3>
          <p><strong>Job Opportunities:</strong> {stats.opportunities || 0}</p>
          <p><strong>Success Stories:</strong> {stats.stories || 0}</p>
          <p><strong>Your Role:</strong> {user.role || 'Unknown'}</p>
        </div>

        {/* Recent Opportunities */}
        <div style={{ padding: '20px', border: '1px solid #ddd', borderRadius: '8px', backgroundColor: '#f8f9fa' }}>
          <h3>Recent Opportunities</h3>
          {recentOpportunities.length > 0 ? (
            recentOpportunities.map(opp => (
              <div key={opp.id} style={{ marginBottom: '10px', padding: '10px', backgroundColor: 'white', borderRadius: '4px' }}>
                <strong>{opp.title}</strong>
                <p style={{ margin: '5px 0', fontSize: '14px' }}>{opp.company}</p>
                <p style={{ margin: '5px 0', fontSize: '12px', color: '#666' }}>{opp.type}</p>
              </div>
            ))
          ) : (
            <p>No opportunities available</p>
          )}
        </div>

        {/* Recent Stories */}
        <div style={{ padding: '20px', border: '1px solid #ddd', borderRadius: '8px', backgroundColor: '#f8f9fa' }}>
          <h3>Recent Success Stories</h3>
          {recentStories.length > 0 ? (
            recentStories.map(story => (
              <div key={story.id} style={{ marginBottom: '10px', padding: '10px', backgroundColor: 'white', borderRadius: '4px' }}>
                <strong>{story.title}</strong>
                <p style={{ margin: '5px 0', fontSize: '14px' }}>By {story.author_name}</p>
                <p style={{ margin: '5px 0', fontSize: '12px', color: '#666' }}>
                  {story.content?.substring(0, 100)}...
                </p>
              </div>
            ))
          ) : (
            <p>No stories available</p>
          )}
        </div>
      </div>

      {/* Quick Actions */}
      <div style={{ marginTop: '30px', padding: '20px', border: '1px solid #ddd', borderRadius: '8px', backgroundColor: '#f8f9fa' }}>
        <h3>Quick Actions</h3>
        <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
          <button 
            onClick={() => window.location.href = '/opportunities'}
            style={{ padding: '10px 20px', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
          >
            Browse Opportunities
          </button>
          <button 
            onClick={() => window.location.href = '/mentorship'}
            style={{ padding: '10px 20px', backgroundColor: '#28a745', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
          >
            Find Mentors
          </button>
          <button 
            onClick={() => window.location.href = '/stories'}
            style={{ padding: '10px 20px', backgroundColor: '#17a2b8', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
          >
            Read Stories
          </button>
        </div>
      </div>
    </div>
  )
}


