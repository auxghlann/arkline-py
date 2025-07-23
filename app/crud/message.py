from sqlalchemy.orm import Session
# from sqlalchemy.exc import NoResultFound
from app.models.models import Message, User, UserRole
from app.schemas.schemas import MessageCreate
from fastapi import HTTPException, status


def create_message(db: Session, sender: User, message_data: MessageCreate):
    db_message = Message(
        sender_id=sender.id,
        receiver_id=message_data.receiver_id,
        subject=message_data.subject,
        body=message_data.body,
        urgency=message_data.urgency if sender.role == UserRole.user else None, # type: ignore
        in_reply_to=message_data.in_reply_to
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def get_message(db: Session, message_id: int, current_user: User):
    message = db.query(Message).filter(
        Message.id == message_id,
        ((Message.sender_id == current_user.id) | (Message.receiver_id == current_user.id)),
        Message.is_deleted == False
    ).first()

    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found or access denied"
        )
    return message


def get_inbox(db: Session, user: User):
    return db.query(Message).filter(
        Message.receiver_id == user.id,
        Message.is_deleted == False
    ).order_by(Message.sent_at.desc()).all()


def delete_message(db: Session, message_id: int, current_user: User):
    message = db.query(Message).filter(
        Message.id == message_id,
        ((Message.sender_id == current_user.id) | (Message.receiver_id == current_user.id)),
        Message.is_deleted == False
    ).first()

    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found or already deleted"
        )

    message.is_deleted = True #type: ignore
    db.commit()
    return {"detail": "Message deleted successfully"}
