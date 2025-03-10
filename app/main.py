import asyncio
from fastapi import FastAPI, Request, WebSocket, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import init_db, get_db
from app.websockets import websocket_endpoint, redis_listener
from app.routes import messages
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

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
async def serve_index(request: Request, session_id: str):
    return templates.TemplateResponse("index.html", {"request": request, "session_id":session_id})

async def start_redis_listener():
    asyncio.create_task(redis_listener())

@app.on_event("startup")
async def startup_event():
    await start_redis_listener()

