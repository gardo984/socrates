from pydantic import BaseModel
from datetime import datetime


class DocumentResponse(BaseModel):
    id: int
    filename: str
    file_type: str | None = None
    file_size: int | None = None
    uploaded_at: datetime
    user_id: int | None = None

    class Config:
        from_attributes = True