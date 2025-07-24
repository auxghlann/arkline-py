from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.crud import message as message_crud
from app.schemas.schema import MessageCreate, MessageRead
from app.db.session import get_db, Base, engine
from app.routers.auth import get_current_user, UserRequest
from app.models.model import User

router = APIRouter(prefix="/messages", tags=["Messages"])

Base.metadata.create_all(bind=engine)

@router.post("/create", response_model=MessageRead)
async def send_message(
    message_data: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # print(current_user)
    result = await message_crud.create_message(db, current_user, message_data)
    return MessageRead(
        id=result.id,
        sender_id=result.sender_id,
        receiver_id=result.receiver_id,
        # receiver_username=result.receiver_username,
        subject=result.subject,
        body=result.body,
        urgency=result.urgency,
        in_reply_to=result.in_reply_to,
        sent_at=result.sent_at,
        is_read=result.is_read,
        is_deleted=result.is_deleted
    )

# @router.get("/{message_id}", response_model=MessageRead)
# async def read_message(
#     message_id: int,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     result = await message_crud.get_message(db, message_id, current_user)
#     return MessageRead(
#         id=result.id,
#         sender_id=result.sender_id,
#         receiver_id=result.receiver_id,
#         subject=result.subject,
#         body=result.body,
#         urgency=result.urgency,
#         in_reply_to=result.in_reply_to,
#         sent_at=result.sent_at,
#         is_read=result.is_read,
#         is_deleted=result.is_deleted
#     )

@router.get("/inbox/", response_model=list[MessageRead])
async def read_inbox(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await message_crud.get_inbox(db, current_user)

@router.delete("/{message_id}")
async def delete_message(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await message_crud.delete_message(db, message_id, current_user)