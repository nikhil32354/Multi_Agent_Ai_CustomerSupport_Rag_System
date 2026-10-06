import React, { useState, useEffect } from 'react'
import Chat from './components/Chat'
import Tickets from './components/Tickets'
import Avatar from './components/Avatar'
import api from './api'

function History({ sessionId }) {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [failed, setFailed] = useState(false)

  useEffect(() => {
    let cancelled = false
    api.history(sessionId)
      .then((history) => {
        if (!cancelled) setItems(history)
      })
      .catch(() => {
        if (!cancelled) setFailed(true)
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })
    return () => { cancelled = true }
  }, [sessionId])

  if (loading) return <div style={{color:'var(--muted)'}}>Loading conversation history…</div>
  if (failed) return <div style={{color:'var(--muted)'}}>Could not load conversation history.</div>
  if (items.length === 0) return <div style={{color:'var(--muted)'}}>No conversation history yet. Messages you send here will appear in this view.</div>

  return <div style={{display:'grid',gap:12}}>
    {items.map((item) => (
      <div className="card" key={item.id}>
        <div style={{display:'flex',justifyContent:'space-between',gap:12,marginBottom:8}}>
          <strong>{item.role === 'user' ? 'You' : 'Assistant'}</strong>
          <span style={{fontSize:12,color:'var(--muted)'}}>{item.created_at ? new Date(item.created_at).toLocaleString() : ''}</span>
        </div>
        <div>{item.content}</div>
      </div>
    ))}
  </div>
}

export default function App() {
  const [sessionId] = useState(() => 'sess-' + Date.now())
  const [activeView, setActiveView] = useState('chat')

    return (
      <div className="app-shell">
        <aside className="sidebar">
          <div className="logo">Agentic Support</div>
          <button className={`nav-item ${activeView === 'chat' ? 'active' : ''}`} onClick={() => setActiveView('chat')}>Chat</button>
          <button className={`nav-item ${activeView === 'tickets' ? 'active' : ''}`} onClick={() => setActiveView('tickets')}>Tickets</button>
          <button className={`nav-item ${activeView === 'history' ? 'active' : ''}`} onClick={() => setActiveView('history')}>History</button>
        </aside>

        <main className="main-panel">
          {activeView === 'chat' ? (
            <>
              <div style={{display:'flex',alignItems:'center',justifyContent:'space-between'}}>
                <div style={{display:'flex',alignItems:'center',gap:12}}>
                  <Avatar size="small" />
                  <h2 style={{margin:0}}>Chat</h2>
                </div>
                <div style={{display:'flex',alignItems:'center',gap:12}}>
                  <div style={{display:'flex',alignItems:'center',gap:8}}>
                    <span className="status-dot" />
                    <div style={{color:'var(--muted)'}}>Online</div>
                  </div>
                  <div className="user-pill">U</div>
                </div>
              </div>
              <div style={{height:18}} />
              <Chat sessionId={sessionId} />
            </>
          ) : activeView === 'tickets' ? (
            <>
              <h2 style={{margin:'0 0 18px'}}>Tickets</h2>
              <Tickets />
            </>
          ) : (
            <>
              <h2 style={{margin:'0 0 18px'}}>Conversation History</h2>
              <History sessionId={sessionId} />
            </>
          )}
        </main>

        {activeView === 'chat' && <aside className="right-panel">
          <div className="card intent-card">
            <div style={{display:'flex',alignItems:'center',gap:12}}>
              <div className="avatar intent-avatar">
                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                  <path d="M12 2L14.3 8.2L21 12L14.3 15.8L12 22L9.7 15.8L3 12L9.7 8.2L12 2Z" fill="white" opacity="0.95"/>
                </svg>
              </div>
              <div style={{flex:1}}>
                <h3 style={{margin:0}}>Intent Agent</h3>
                <p style={{color:'var(--muted)',margin:'6px 0 0'}}>I read the user query first and route it to the correct agent.</p>
              </div>
            </div>
            <ul className="faq-list" style={{marginTop:12}}>
              <li>Greeting → direct response</li>
              <li>FAQ question → FAQ Agent</li>
              <li>Unresolved issue → Ticket Agent</li>
            </ul>
          </div>
          <div className="card">
            <div style={{display:'flex',alignItems:'center',gap:12}}>
              <Avatar />
              <div style={{flex:1}}>
                <h3 style={{margin:0}}>FAQ Agent (RAG)</h3>
                <p style={{color:'var(--muted)',margin:'6px 0 0'}}>I search the knowledge base to answer your questions.</p>
              </div>
            </div>
            <ul className="faq-list" style={{marginTop:12}}>
              <li>What is the refund policy?</li>
              <li>How can I cancel my order?</li>
              <li>What are the delivery times?</li>
            </ul>
          </div>
          <div className="card">
            <div style={{display:'flex',alignItems:'center',gap:12}}>
              <Avatar />
              <div style={{flex:1}}>
                <h3 style={{margin:0}}>Ticket Agent</h3>
                <p style={{color:'var(--muted)',margin:'6px 0 0'}}>I create a support ticket if your issue needs human assistance.</p>
              </div>
            </div>
            <div style={{height:12}} />
            <Tickets />
          </div>
        </aside>}
      </div>
    )
}
