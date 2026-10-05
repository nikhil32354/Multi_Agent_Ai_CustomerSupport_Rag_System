import React, { useEffect, useState } from 'react'
import api from '../api'

export default function Tickets(){
  const [tickets, setTickets] = useState([])

  useEffect(()=>{ api.tickets().then(setTickets).catch(()=>{}) }, [])

  return (
    <div>
      <h4 style={{marginTop:0}}>Recent Tickets</h4>
      {tickets.length===0 && <div style={{color:'var(--muted)'}}>No recent tickets</div>}
      {tickets.map(t=> (
        <div key={t.id} className="card" style={{padding:10, display:'flex',justifyContent:'space-between',alignItems:'center'}}>
          <div>
            <div style={{fontWeight:700,marginBottom:6}}>{t.title}</div>
            <div style={{fontSize:13,color:'var(--muted)'}}>{t.description}</div>
            <div style={{fontSize:12,color:'var(--muted)',marginTop:8}}>Created: {new Date(t.created_at).toLocaleString?.() || t.created_at}</div>
          </div>
          <div style={{textAlign:'right'}}>
            <div style={{fontSize:12, color: t.status==='open' ? '#ff6b6b' : '#9ad3bc', fontWeight:700}}>{t.status}</div>
          </div>
        </div>
      ))}
      <div style={{marginTop:8,textAlign:'right'}}>
        <a href="#" style={{color:'var(--accent)',textDecoration:'none'}}>View All Tickets →</a>
      </div>
    </div>
  )
}
