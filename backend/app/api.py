from fastapi import APIRouter, Depends, HTTPException
import os
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .db import get_db
from . import crud, services
from .schemas import MessageCreate, TicketCreate, TicketOut
from .core.config import settings

router = APIRouter()


def init_cors(app):
    allowed_origins = [
        'http://localhost:3000',
        'http://localhost:3001',
        'http://localhost:5173',
    ]
    if settings.frontend_origin:
        allowed_origins.append(settings.frontend_origin.rstrip('/'))

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )


@router.post('/chat')
def chat(payload: MessageCreate, db: Session = Depends(get_db)):
    crud.add_message(db, payload.session_id, 'user', payload.content)
    # route intent
    intent = services.IntentAgent.route(payload.content)
    if intent == 'faq':
        faq = services.FAQAgent()
        answer = faq.answer(payload.content)
        crud.add_message(db, payload.session_id, 'assistant', answer)
        return {'intent': 'faq', 'answer': answer}
    else:
        ticket_agent = services.TicketAgent(db)
        t = ticket_agent.create_ticket(title=f'From chat: {payload.content[:100]}', description=payload.content)
        msg = f'Ticket created successfully. Ticket ID: #{t.id}. Status: {t.status}.'
        crud.add_message(db, payload.session_id, 'assistant', msg)
        return {'intent': 'ticket', 'ticket': TicketOut.model_validate(t)}


# Upload endpoint removed — knowledge base is hosted on backend under backend/knowledge_base


@router.post('/ticket', response_model=TicketOut)
def create_ticket(t: TicketCreate, db: Session = Depends(get_db)):
    return crud.create_ticket(db, title=t.title, description=t.description)


@router.get('/tickets')
def list_tickets(db: Session = Depends(get_db)):
    return crud.list_tickets(db)


@router.get('/history/{session_id}')
def history(session_id: str, db: Session = Depends(get_db)):
    return crud.get_history(db, session_id)
