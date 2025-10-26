from pydantic import BaseModel, Field
from typing import Literal

class ChatMessage(BaseModel):

    role: Literal["system", "user", "assistant"] = Field(..., required=True, description="Role of the message sender")
    content: str = Field(..., required=True, description="Content of the message")

    def to_dict(self) -> dict:
        return {"role": self.role, "content": self.content}