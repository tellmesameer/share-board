from fastapi import FastAPI, Request, WebSocket, Depends, Form
from app.routes import messages
from app.websockets import websocket_endpoint
from app.database import init_db, get_db
from app.crud import fetch_existing_session, save_message
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

templates = Jinja2Templates(directory="app/templates")

# Serve static files if you have CSS/JS
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.on_event("startup")
async def startup():
    await init_db()  # Initialize database

# Include API routes
app.include_router(messages.router, prefix="")

# WebSocket endpoint
app.add_api_websocket_route("/ws/{session_id}", websocket_endpoint)


@app.get("/{session_id}")
async def serve_index(request: Request, session_id: str, db: AsyncSession = Depends(get_db)):
    message = await fetch_existing_session(db, session_id) # Fetch messages from the database
    try:
        message = message.text
    except:
        message = ""
    return templates.TemplateResponse("index.html", {"request": request, "session_id":session_id, "existing_session_message": message})


@app.post("/{session_id}")
async def save_message_endpoint(session_id: str, message: str = Form(...), db: AsyncSession = Depends(get_db)):
    await save_message(db, session_id, message)
    return {"status": "success", "message": "Message saved"}


