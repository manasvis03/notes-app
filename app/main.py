from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import os

from . import db, embeddings, vector_store

app = FastAPI(title="Notes App with AI Search")
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")

# Initialize on startup
DB_DIM = 384
vs = None


# ===== PYDANTIC MODELS =====
class NoteIn(BaseModel):
    title: str
    content: str
    tags: str = ""
    category: str = ""


@app.on_event("startup")
def startup():
    global vs
    db.init_db()
    model = embeddings.get_model()
    # model output dim
    dim = model.get_sentence_embedding_dimension()
    vs = vector_store.VectorStore(dim=dim)


# ===== NOTE ENDPOINTS =====
@app.post("/notes")
def create_note(note: NoteIn):
    nid = db.add_note(note.title, note.content, note.tags, note.category)
    text = f"{note.title}. {note.content} {note.tags}"
    emb = embeddings.embed_text(text)
    vs.add(emb, nid)
    return {"id": nid}


@app.get("/notes")
def get_notes():
    return db.list_notes()


@app.get("/notes/{note_id}")
def get_note_detail(note_id: int):
    note = db.get_note(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@app.put("/notes/{note_id}")
def update_note(note_id: int, note: NoteIn):
    if not db.get_note(note_id):
        raise HTTPException(status_code=404, detail="Note not found")
    success = db.update_note(note_id, note.title, note.content, note.tags, note.category)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to update note")
    # Update embedding
    text = f"{note.title}. {note.content} {note.tags}"
    emb = embeddings.embed_text(text)
    vs.update(note_id, emb)
    return {"id": note_id, "title": note.title, "content": note.content, "tags": note.tags, "category": note.category}


@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    if not db.get_note(note_id):
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete_note(note_id)
    vs.delete(note_id)
    return {"success": True}


@app.get("/search")
def search(q: str = "", search_type: str = "semantic", k: int = 5):
    """
    Search notes by keyword or semantic meaning.
    search_type: 'keyword' or 'semantic'
    """
    if not q:
        raise HTTPException(status_code=400, detail="Query parameter 'q' required")
    
    if search_type == "keyword":
        # Simple keyword search
        all_notes = db.list_notes()
        q_lower = q.lower()
        results = []
        for note in all_notes:
            if q_lower in note["title"].lower() or q_lower in note["content"].lower() or q_lower in note["tags"].lower():
                results.append(note)
        return results[:k]
    else:
        # Semantic search
        emb = embeddings.embed_text(q)
        hits = vs.search(emb, top_k=k)
        results = []
        for nid, score in hits:
            note = db.get_note(nid)
            if note:
                note["score"] = score
                results.append(note)
        return results


@app.get("/tags")
def get_tags():
    return {"tags": db.get_all_tags()}


@app.get("/categories")
def get_categories():
    return {"categories": db.get_all_categories()}


@app.get("/filter/tag/{tag}")
def filter_by_tag(tag: str):
    return db.filter_notes_by_tag(tag)


@app.get("/filter/category/{category}")
def filter_by_category(category: str):
    return db.filter_notes_by_category(category)


@app.get("/", response_class=HTMLResponse)
def homepage():
    with open(os.path.join(os.path.dirname(__file__), "static", "index.html"), "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())
