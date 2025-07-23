from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from enum import Enum
from datetime import datetime


# --- Enums ---

class UserRole(str, Enum):
    user = "user"
    admin = "admin"

class UrgencyLevel(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"


# --- User Schemas ---

class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None

class UserCreate(UserBase):
    password: str  # optional: add password hashing in backend

class UserRead(UserBase):
    id: int
    role: UserRole
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# --- Message Schemas ---

class MessageBase(BaseModel):
    subject: Optional[str] = None
    body: str
    urgency: Optional[UrgencyLevel] = None 
    in_reply_to: Optional[int] = None  # For replies

# --- Message Create Schema (Children) ---
class MessageCreate(MessageBase):
    receiver_id: int

class MessageRead(MessageBase):
    id: int
    sender_id: int
    receiver_id: int
    sent_at: datetime
    is_read: bool
    # is_archived: bool
    is_deleted: bool

    model_config = ConfigDict(from_attributes=True)
