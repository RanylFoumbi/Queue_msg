from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field

class Message(BaseModel):
    content: str
    user_name: str
    sent_at: Optional[str] = Field(default_factory=lambda: datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M:%S"))

    def to_dict(self):
        return {
            "content": self.content,
            "user_name": self.user_name,
            "sent_at": self.sent_at
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            content=data["content"],
            user_name=data["user_name"],
            sent_at=data["sent_at"]
        )