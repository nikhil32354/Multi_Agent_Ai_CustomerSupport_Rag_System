import React, { useState, useEffect } from 'react'
import api from '../api'
import Avatar from './Avatar'

export default function Chat({ sessionId }){
  const [messages, setMessages] = useState([])
  const [text, setText] = useState('')
  const endRef = React.useRef(null)

  useEffect(()=>{
    // load history then show welcome if empty
    api.history(sessionId).then((hist)=>{
      if(!hist || hist.length===0){
        setMessages([{ role:'assistant', content: 'Hi Sir! 👋\nHow can I help you today?', created_at: '' }])
      } else {
        setMessages(hist.map(h=>({role:h.role, content:h.content, created_at: h.created_at})))
      }
    }).catch(()=>{
      setMessages([{ role:'assistant', content: 'Hi Sir! 👋\nHow can I help you today?', created_at: '' }])
    })
  },[sessionId])

  useEffect(()=>{
    // scroll to bottom when messages update
    if(endRef.current) endRef.current.scrollIntoView({ behavior: 'smooth', block: 'end' })
  },[messages])

  async function send(){
    if(!text) return

    const prompts = text
      .split(/\n+/)
      .map((value) => value.trim())
      .filter(Boolean)

    setText('')

    for (const prompt of prompts) {
      const userMsg = { session_id: sessionId, role: 'user', content: prompt }
      setMessages(m => [...m, {role:'user', content:prompt, created_at: ''}])

      try{
        const res = await api.chat(userMsg)
        if(res.intent === 'general' || res.intent === 'faq'){
          setMessages(m => [...m, {role:'assistant', content: res.answer}])
        } else if(res.intent === 'ticket'){
          setMessages(m => [...m, {
            role:'assistant',
            content: res.answer || 'Human assistance is needed for your query. I have created a support ticket for you.',
            ticket:res.ticket,
          }])
        }
      }catch(err){
        setMessages(m => [...m, {role:'assistant', content: 'Sorry, there was an error contacting the server.'}])
      }
    }
  }

  return (
    <div style={{display:'flex',flexDirection:'column',height:'70vh'}}>
      <div className="chat-window">
        {messages.map((m,i)=>(
          <div key={i} className={`message ${m.role==='assistant'?'assistant':'user'}`}>
            {m.role==='assistant' && <div style={{marginRight:12}}>
              <Avatar size="small" />
            </div>}

            <div style={{display:'flex',flexDirection:'column',maxWidth:'74%'}}>
              {m.role==='assistant' ? (
                <>
                  {/* Assistant bubble */}
                  <div className={`bubble assistant-bubble`}>{m.content}</div>
                  {m.ticket && (
                    <div className="ticket-created">
                      <div className="ticket-created-title">Ticket Created</div>
                      <div className="ticket-meta">Ticket ID: <strong>#{m.ticket.id}</strong></div>
                      <div className="ticket-status">Status: <span className={m.ticket.status === 'open' ? 'open' : ''}>{m.ticket.status}</span></div>
                    </div>
                  )}
                </>
              ) : (
                <div style={{display:'flex',flexDirection:'column',alignItems:'flex-end'}}>
                  <div className={`bubble user`}>{m.content}</div>
                </div>
              )}
              <div className="ts">{m.created_at || ''}</div>
            </div>
          </div>
        ))}
        <div ref={endRef} />
      </div>

      <div className="composer">
        <input value={text} onChange={e=>setText(e.target.value)} placeholder="Type your message..." />
        <button onClick={send} aria-label="Send message">
          <svg viewBox="0 0 24 24" width="18" height="18" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M2 21L23 12 2 3 2 10l15 2-15 2 0 4z" fill="#fff" opacity="0.9"/>
          </svg>
        </button>
      </div>
    </div>
  )
}
