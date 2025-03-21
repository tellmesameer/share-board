import logging  # added logging import
from fastapi import WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.crud import save_message

# Store active connections for each session
active_sessions: dict[str, list[WebSocket]] = {}

async def websocket_endpoint(websocket: WebSocket, session_id: str, db: AsyncSession = Depends(get_db)):
    await websocket.accept()
    logging.info(f"WebSocket connection accepted for session {session_id}")  # added log

    # Add the current connection to the session
    if session_id not in active_sessions:
        active_sessions[session_id] = []
    active_sessions[session_id].append(websocket)

    try:
        while True:
            text = await websocket.receive_text()
            logging.info(f"Received message in session {session_id}: {text}")  # added log

            # Broadcast the message to all connected clients in the session
            for client in active_sessions[session_id]:
                if client != websocket:  # Don't send back to the sender
                    await client.send_text(text)

    except WebSocketDisconnect:
        logging.info(f"Client disconnected from session {session_id}")  # added log
        # Remove the connection from the session
        if session_id in active_sessions:
            active_sessions[session_id].remove(websocket)
        # await websocket.close()