from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.crud import get_messages



router = APIRouter()

@router.get("/history/{session_id}")
async def get_history(session_id: str, db: AsyncSession = Depends(get_db)):
    messages = await get_messages(db, session_id)
    return {"session_id": session_id, "messages": [msg.text for msg in messages]}



