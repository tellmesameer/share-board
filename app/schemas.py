from pydantic import BaseModel

class MessageSchema(BaseModel):
    session_id: str
    text: str
