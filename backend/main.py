from fastapi import FastAPI, Depends, HTTPException
from contextlib import asynccontextmanager
import os
import psycopg
from psycopg.rows import dict_row

from pydantic import BaseModel

from graph.builder import build_graph, HAS_POSTGRES

class DBConnectionManager:
    def __init__(self):
        self.conn = None

    def connect(self):
        db_user = os.getenv("POSTGRES_USER", "postgres")
        db_pass = os.getenv("POSTGRES_PASSWORD", "postgres")
        db_host = os.getenv("POSTGRES_HOST", "localhost")
        db_port = os.getenv("POSTGRES_PORT", "5432")
        db_name = os.getenv("POSTGRES_DB", "travel_agent")
        
        conn_info = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
        
        try:
            self.conn = psycopg.connect(conn_info, row_factory=dict_row)
            return self.conn
        except Exception as e:
            print(f"Failed to connect to Postgres: {e}")
            return None

    def get_conn(self):
        return self.conn

    def close(self):
        if self.conn:
            self.conn.close()

db_manager = DBConnectionManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup DB connection
    db_manager.connect()
    yield
    # Teardown
    db_manager.close()

app = FastAPI(
    title="Travel Agent API",
    description="Industrial FastAPI backend for the Multi-Modal Travel Assistant",
    version="1.0.0",
    lifespan=lifespan
)

class ChatRequest(BaseModel):
    thread_id: str
    message: str

class ChatResponse(BaseModel):
    response: str
    thread_id: str

@app.get("/health")
def health_check():
    return {"status": "ok", "postgres_enabled": HAS_POSTGRES, "db_connected": db_manager.get_conn() is not None}

from fastapi.responses import StreamingResponse
import json

@app.post("/chat/stream")
async def chat_stream_endpoint(request: ChatRequest):
    conn = db_manager.get_conn()
    graph = build_graph(conn)
    config = {"configurable": {"thread_id": request.thread_id}}
    input_state = {"messages": [("user", request.message)], "query": request.message}
    
    async def event_stream():
        for event in graph.stream(input_state, config=config, stream_mode="updates"):
            # Serialize event dict to JSON
            yield f"data: {json.dumps(event, default=str)}\n\n"
    
    return StreamingResponse(event_stream(), media_type="text/event-stream")

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    conn = db_manager.get_conn()
    graph = build_graph(conn)
    
    config = {"configurable": {"thread_id": request.thread_id}}
    
    input_state = {"messages": [("user", request.message)], "query": request.message}
    
    try:
        result = graph.invoke(input_state, config=config)
        final_message = result.get("final_response", {})
        return ChatResponse(response=str(final_message), thread_id=request.thread_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

