from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from enum import Enum
from datetime import datetime


# --- Enums ---

class UserRole(str, Enum):
    user = "user"
    admin = "admin"

class UrgencyLevel(str, Enum):
    high = "High"
    medium = "Medium"
    low = "Low"


# --- User Schemas ---

class UserBase(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class UserCreate(UserBase):
    username: str
    password: str
    role: Optional[UserRole] = UserRole.user
    created_at: datetime

class UserRead(UserBase):
    id: int
    role: UserRole
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# --- Message Schemas ---

class MessageBase(BaseModel):
    subject: Optional[str] = None
    body: str
    # urgency: Optional[UrgencyLevel] = None 
    in_reply_to: Optional[int] = None  # For replies

# --- Message Create Schema (Children) ---
class MessageCreate(MessageBase):
    receiver_username: str
    # urgency: UrgencyLevel

class MessageRead(MessageBase):
    id: int
    sender_id: int
    # receiver_username: str
    sent_at: datetime
    is_read: bool
    # is_archived: bool
    urgency: UrgencyLevel
    is_deleted: bool

    model_config = ConfigDict(from_attributes=True)
