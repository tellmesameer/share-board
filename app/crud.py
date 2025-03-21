from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.models import Message



async def fetch_existing_session(db: AsyncSession, session_id: str):
    existing_message = await db.execute(
        select(Message).where(Message.session_id == session_id)
    )
    existing_message = existing_message.scalars().first()

    return existing_message


async def save_message(db: AsyncSession, session_id: str, text: str):
    # Check if a message with the session_id already exists
    existing_message = await fetch_existing_session(db, session_id)

    if existing_message:
        # Update the existing message
        existing_message.text = text
        await db.commit()
        await db.refresh(existing_message)  # Refresh to get the latest state
        return existing_message
    else:
        # Create a new message
        new_message = Message(session_id=session_id, text=text)
        db.add(new_message)
        await db.commit()
        await db.refresh(new_message)
        return new_message

async def get_messages(db: AsyncSession, session_id: str):
    result = await db.execute(select(Message).where(Message.session_id == session_id))
    return result.scalars().all()
