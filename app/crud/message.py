from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.model import Message, User, UserRole, UrgencyLevel
from app.schemas.schema import MessageCreate
from app.client.arkline_ai import ArklineAI


# -- Helper --
async def get_urgency_classification(text: str) -> UrgencyLevel:
    client = ArklineAI()
    response = client.get_response(text)
    label = response['urgency'].lower()

    match label:
        case "high":
            return UrgencyLevel.high
        case "medium":
            return UrgencyLevel.medium
        case "low":
            return UrgencyLevel.low


# -- CRUD: Create --
async def create_message(db: Session, sender: User, message_data: MessageCreate) -> Message:

    urgency = await get_urgency_classification(message_data.body)

    receiver_id_tuple = db.query(User.id).filter(
        User.username == message_data.receiver_username
    ).first()
    if not receiver_id_tuple:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Receiver not found"
        )
    receiver_id = receiver_id_tuple[0]

    db_message = Message(
        sender_id=sender.id,
        receiver_id=receiver_id,
        subject=message_data.subject,
        body=message_data.body,
        urgency=urgency,
        in_reply_to=message_data.in_reply_to
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


# -- CRUD: Get Single Message --
async def get_message(db: Session, message_id: int, current_user: User) -> Message:
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


# -- CRUD: Inbox --
async def get_inbox(db: Session, user: User) -> list[Message]:
    return db.query(Message).filter(
        Message.receiver_id == user.id,
        Message.is_deleted == False
    ).order_by(Message.sent_at.desc()).all()


# -- CRUD: Delete --
async def delete_message(db: Session, message_id: int, current_user: User) -> dict:
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

    message.is_deleted = True
    db.commit()
    return {"detail": "Message deleted successfully"}
