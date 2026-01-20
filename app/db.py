import sqlite3
from typing import List, Dict, Optional
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "notes.db")

def init_db() -> None:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Create notes table (no user_id needed)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        content TEXT,
        tags TEXT,
        category TEXT
    )
    """)
    conn.commit()
    conn.close()
# ===== NOTE FUNCTIONS =====
def add_note(title: str, content: str, tags: str = "", category: str = "") -> int:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO notes (title, content, tags, category) VALUES (?, ?, ?, ?)", (title, content, tags, category))
    nid = cur.lastrowid
    conn.commit()
    conn.close()
    return nid

def list_notes() -> List[Dict]:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, title, content, tags, category FROM notes ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return [{"id": r[0], "title": r[1], "content": r[2], "tags": r[3] or "", "category": r[4] or ""} for r in rows]

def get_note(note_id: int) -> Optional[Dict]:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, title, content, tags, category FROM notes WHERE id = ?", (note_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    return {"id": row[0], "title": row[1], "content": row[2], "tags": row[3] or "", "category": row[4] or ""}

def update_note(note_id: int, title: str, content: str, tags: str = "", category: str = "") -> bool:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("UPDATE notes SET title = ?, content = ?, tags = ?, category = ? WHERE id = ?", (title, content, tags, category, note_id))
    conn.commit()
    success = cur.rowcount > 0
    conn.close()
    return success

def delete_note(note_id: int) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    success = cur.rowcount > 0
    conn.close()
    return success

def get_all_tags() -> List[str]:
    """Get all unique tags from notes"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT tags FROM notes WHERE tags IS NOT NULL AND tags != ''")
    rows = cur.fetchall()
    conn.close()
    tags_set = set()
    for row in rows:
        if row[0]:
            tags = [t.strip() for t in row[0].split(',')]
            tags_set.update(tags)
    return sorted(list(tags_set))

def get_all_categories() -> List[str]:
    """Get all unique categories"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT category FROM notes WHERE category IS NOT NULL AND category != '' ORDER BY category")
    rows = cur.fetchall()
    conn.close()
    return [r[0] for r in rows]

def filter_notes_by_tag(tag: str) -> List[Dict]:
    """Get notes with a specific tag"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, title, content, tags, category FROM notes WHERE tags LIKE ? ORDER BY id DESC", (f'%{tag}%',))
    rows = cur.fetchall()
    conn.close()
    return [{"id": r[0], "title": r[1], "content": r[2], "tags": r[3] or "", "category": r[4] or ""} for r in rows]

def filter_notes_by_category(category: str) -> List[Dict]:
    """Get notes with a specific category"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, title, content, tags, category FROM notes WHERE category = ? ORDER BY id DESC", (category,))
    rows = cur.fetchall()
    conn.close()
    return [{"id": r[0], "title": r[1], "content": r[2], "tags": r[3] or "", "category": r[4] or ""} for r in rows]
