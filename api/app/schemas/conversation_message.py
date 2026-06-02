from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any


# --- Conversation Schemas ---
class ConversationCreate(BaseModel):
    document_id: int
    title: Optional[str] = "New Conversation"


class ConversationUpdate(BaseModel):
    title: Optional[str] = None


class ConversationResponse(BaseModel):
    id: int
    document_id: int
    title: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# --- Message Schemas ---
class MessageCreate(BaseModel):
    conversation_id: int
    role: str = Field(..., pattern="^(user|assistant)$", description="Role can be 'user' or 'assistant'")
    content: str
    metadata_: Optional[Dict[str, Any]] = None


class MessageUpdate(BaseModel):
    content: Optional[str] = None
    metadata_: Optional[Dict[str, Any]] = None


class MessageResponse(BaseModel):
    id: int
    conversation_id: int
    role: str
    content: str
    created_at: datetime
    metadata_: Optional[Dict[str, Any]] = Field(None, alias="metadata")

    class Config:
        from_attributes = True
        populate_by_name = True # Allow setting by alias