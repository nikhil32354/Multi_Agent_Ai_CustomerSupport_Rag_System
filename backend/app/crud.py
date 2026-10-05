from sqlalchemy.orm import Session
from . import models


def create_ticket(db: Session, title: str, description: str | None = None):
    t = models.Ticket(title=title, description=description)
    db.add(t)
    db.commit()
    db.refresh(t)
    return t


def list_tickets(db: Session):
    return db.query(models.Ticket).order_by(models.Ticket.created_at.desc()).all()


def add_message(db: Session, session_id: str, role: str, content: str):
    m = models.Message(session_id=session_id, role=role, content=content)
    db.add(m)
    db.commit()
    db.refresh(m)
    return m


def get_history(db: Session, session_id: str):
    return db.query(models.Message).filter(models.Message.session_id == session_id).order_by(models.Message.created_at).all()
