import asyncio
import json
import redis

from fastapi import WebSocket, WebSocketDisconnect, Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.crud import save_message
from typing import Dict, List

# Redis configuration
REDIS_HOST = "shareboard-redis-cpfi-cgfc-935606.leapcell.cloud"  # Replace with your Redis host
REDIS_PORT = 6379         # Replace with your Redis port
REDIS_CHANNEL = "chat"    # Channel for broadcasting messages

# Initialize Redis connection
redis_client = redis.Redis.from_url("redis://default:KoHywQUi0c58nqwbSGZIyzZU53TJeJKT@redis-17640.c270.us-east-1-3.ec2.redns.redis-cloud.com:17640")
# Initialize Redis Pub/Sub
pubsub = redis_client.pubsub()
pubsub.subscribe(REDIS_CHANNEL)
print(f"Subscribed to Redis channel: {REDIS_CHANNEL}")

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        if session_id not in self.active_connections:
            self.active_connections[session_id] = []
        self.active_connections[session_id].append(websocket)
        print(f"WebSocket connected to session: {session_id}, Total connections: {len(self.active_connections[session_id])}")


    def disconnect(self, websocket: WebSocket, session_id: str):
        if session_id in self.active_connections and websocket in self.active_connections[session_id]:
            self.active_connections[session_id].remove(websocket)
            print(f"WebSocket disconnected from session: {session_id}, Remaining connections: {len(self.active_connections[session_id]) if session_id in self.active_connections else 0}")
            if not self.active_connections[session_id]:
                del self.active_connections[session_id]
                print(f"Session {session_id} has no more connections, removing it.")
        else:
            print(f"WebSocket disconnect: Session {session_id} or WebSocket not found in active connections.")


    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, session_id: str):
        # Publish message to Redis
        try:
            redis_client.publish(REDIS_CHANNEL, json.dumps({"session_id": session_id, "message": message}))
            print(f"Published message to Redis channel {REDIS_CHANNEL}: Session ID={session_id}, Message={message}")
        except redis.exceptions.RedisError as e:
            print(f"Error publishing to Redis: {e}")

manager = ConnectionManager()

async def redis_listener(db: AsyncSession = Depends(get_db)):  # Add Depends(get_db)
    print("Redis listener started")
    while True:
        try:
            message = pubsub.get_message()
            if message:
                print(f"Raw Redis message: {message}")  # Print the raw message

            if message and message["type"] == "message":
                try:
                    data = json.loads(message["data"].decode("utf-8"))
                    session_id = data["session_id"]
                    message_text = data["message"]
                    print(f"Received Redis message: Session ID={session_id}, Message={message_text}")

                    if session_id in manager.active_connections:
                        print(f"Active connections for session {session_id}: {len(manager.active_connections[session_id])}")
                        for connection in manager.active_connections[session_id]:
                            try:
                                print(f"Sending message to WebSocket: {message_text}")
                                await connection.send_text(message_text)
                                print(f"Message sent successfully to WebSocket.")
                            except Exception as e:
                                print(f"Error sending message to WebSocket: {e}")
                    else:
                        print(f"No active connections for session {session_id}")

                    # Save message to database
                    # try:
                    #     await save_message(db, session_id, message_text)
                    #     print(f"Message saved to database successfully.")
                    # except Exception as e:
                    #     print(f"Error saving message to database: {e}")

                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}, Raw data: {message['data']}")
                except Exception as e:
                    print(f"General error processing message: {e}")


        except redis.exceptions.RedisError as e:
            print(f"Error receiving from Redis: {e}")
        except Exception as e:
            print(f"General error in redis_listener: {e}")

        await asyncio.sleep(0.01)  # Avoid busy-waiting

async def websocket_endpoint(websocket: WebSocket, session_id: str, db: AsyncSession = Depends(get_db)):
    await manager.connect(websocket, session_id)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received data from WebSocket: {data}, Session ID: {session_id}")
            await manager.broadcast(data, session_id)  # No longer need to await here
    except Exception as e:
        print(f"Error in websocket_endpoint: {e}")
    finally:
        manager.disconnect(websocket, session_id)