import uuid
from datetime import datetime
from typing import Optional
from pydantic import UUID4
from pydantic.main import BaseModel, Field




class DocumentInput(BaseModel):
    """DocumentInput model."""
    id: UUID4 = Field(default_factory=uuid.uuid4)
    title: str
    content: str
    file_type: str
    created_at: datetime = Field(default_factory=datetime.now)