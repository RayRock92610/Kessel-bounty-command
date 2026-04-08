from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import json

app = FastAPI(title="Blood Moon Persistence API")
DB_PATH = "blood_moon.db"

class StateUpdate(BaseModel):
    agent_id: str
    state_blob: dict
    security_hash: str

@app.post("/state/update")
async def update_state(update: StateUpdate):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO state_logs (agent_id, state_blob, security_hash) VALUES (?, ?, ?)",
            (update.agent_id, json.dumps(update.state_blob), update.security_hash)
        )
        conn.commit()
        conn.close()
        return {"status": "success", "agent": update.agent_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/state/{agent_id}")
async def get_latest_state(agent_id: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT state_blob FROM state_logs WHERE agent_id = ? ORDER BY timestamp DESC LIMIT 1",
        (agent_id,)
    )
    result = cursor.fetchone()
    conn.close()
    if result:
        return json.loads(result[0])
    raise HTTPException(status_code=404, detail="State not found")
