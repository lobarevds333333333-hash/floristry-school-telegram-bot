import aiosqlite
from datetime import datetime
from typing import Optional, Dict, Any
from config import DB_PATH

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lead_code TEXT UNIQUE NOT NULL,
                user_id INTEGER NOT NULL,
                username TEXT,
                full_name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT NOT NULL,
                course TEXT NOT NULL,
                crm_status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()

async def save_lead(
    user_id: int,
    username: Optional[str],
    full_name: str,
    phone: str,
    email: str,
    course: str
) -> Dict[str, Any]:
    """
    Saves lead to local SQLite DB and returns a dictionary with generated lead_code.
    """
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT COUNT(*) FROM leads")
        row = await cursor.fetchone()
        next_num = (row[0] if row else 0) + 1001
        lead_code = f"FL-{next_num}"
        
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await db.execute("""
            INSERT INTO leads (lead_code, user_id, username, full_name, phone, email, course, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (lead_code, user_id, username or "", full_name, phone, email, course, now))
        await db.commit()

        return {
            "lead_code": lead_code,
            "user_id": user_id,
            "username": username,
            "full_name": full_name,
            "phone": phone,
            "email": email,
            "course": course,
            "created_at": now
        }

async def update_crm_status(lead_code: str, status: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE leads SET crm_status = ? WHERE lead_code = ?",
            (status, lead_code)
        )
        await db.commit()
