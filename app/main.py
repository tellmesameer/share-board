import io
import contextlib
import subprocess
import logging
from app.routes import messages
from app.models import CodeRequest
from fastapi import FastAPI, Request
from app.database import init_db, get_db
from fastapi.staticfiles import StaticFiles
from app.websockets import websocket_endpoint
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.middleware.cors import CORSMiddleware
from app.crud import fetch_existing_session, save_message
from fastapi import FastAPI, Request, WebSocket, Depends, Form

logging.basicConfig(level=logging.DEBUG)

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
    if message:
        message = message.text
    else:
        message = ""
    return templates.TemplateResponse("index.html", {"request": request, "session_id":session_id, "existing_session_message": message})


@app.post("/{session_id}")
async def save_message_endpoint(session_id: str, message: str = Form(...), db: AsyncSession = Depends(get_db)):
    await save_message(db, session_id, message)
    return {"status": "success", "message": "Message saved"}




@app.post("/ide/python")
def run_code(request: CodeRequest):
    """
    Executes the provided Python code using exec() and captures output.
    WARNING: Running arbitrary code in your server environment is dangerous.
    """
    logging.info("Received code to execute: %s", request.code)
    try:
        stdout_buffer = io.StringIO()
        exec_globals = {}
        with contextlib.redirect_stdout(stdout_buffer):
            exec(request.code, exec_globals)
        output = stdout_buffer.getvalue()
        logging.debug("Execution output: %r", output)
        return {"output": output}
    except Exception as e:
        logging.error("Error executing code: %s", str(e), exc_info=True)
        return {"output": str(e)}
    
    
############################################