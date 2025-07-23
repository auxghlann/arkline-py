from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base
import enum

# --- Enum definitions ---

class UserRole(enum.Enum):
    user = "user"
    admin = "admin"

class UrgencyLevel(enum.Enum):
    high = "high"
    medium = "medium"
    low = "low"

# --- Models ---

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    name = Column(String(100))
    role = Column(Enum(UserRole), default=UserRole.user, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    sent_messages = relationship("Message", back_populates="sender", foreign_keys="Message.sender_id")
    received_messages = relationship("Message", back_populates="receiver", foreign_keys="Message.receiver_id")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    subject = Column(Text)
    body = Column(Text)
    urgency = Column(Enum(UrgencyLevel), nullable=False, default=UrgencyLevel.medium)

    sent_at = Column(DateTime(timezone=True), server_default=func.now())
    in_reply_to = Column(Integer, ForeignKey("messages.id"), nullable=True)

    is_read = Column(Boolean, default=False)
    # is_archived = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)

    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_messages")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="received_messages")
    parent_message = relationship("Message", remote_side=[id])  # For threading
