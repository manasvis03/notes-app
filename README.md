# Smart Notes App with AI Search

A beautiful, feature-rich notes application with AI-powered semantic search, built with FastAPI and vanilla JavaScript.
Features

Core Features
- **Create Notes** - Add notes with title, content, tags, and category
- **Edit Notes** - Update notes inline with a beautiful interface
- **Delete Notes** - Remove notes you no longer need
- **View All Notes** - Browse all your notes in one place
Search & Discovery
- **Semantic Search** - AI-powered search that understands meaning, not just keywords
  - Finds notes by concept and intent
  - Relevance scoring
  - Uses SentenceTransformers embeddings
Keyword Search** - Fast exact-match searching
  - Search by title, content, or tags
  - Find exact text matches
Organization
- **Tags** - Add comma-separated tags to organize notes
  - Auto-generated filter buttons
  - Quick filtering by tag

Organize notes by category
  - Built-in categories: Personal, Work, Study, Ideas, Tasks
  - Quick filtering by category

 Technical Features
- **Beautiful UI** - Modern gradient design with animations
- **Responsive** - Works on desktop and mobile
- **Fast** - Instant note creation and updates
- **No Authentication** - Simple, direct access to your notes
- **Persistent Storage** - SQLite database with vector embeddings

 Installation

### Prerequisites
- Python 3.8+
- pip or conda

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Start the Server
```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### Step 3: Access the App
Open your browser and go to: **http://127.0.0.1:8000**

## Usage

### Creating a Note
1. Click the **Create** tab
2. Enter note title and content
3. (Optional) Select a category
4. (Optional) Add tags (comma-separated)
5. Click **Add Note**

### Searching Notes

#### Semantic Search (Recommended)
1. Click the **Search** tab
2. Make sure **Semantic (by meaning)** is selected
3. Type what you're looking for: "python tutorials", "meeting notes", etc.
4. Click **Search**

#### Keyword Search
1. Click the **Search** tab
2. Select **Keyword (exact match)**
3. Type exact text to search
4. Click **Search**

### Filtering Notes
1. Click the **View All** tab
2. Click tag filters under "Tags:" section
3. Or click category filters under "Categories:" section
4. Click **Clear Filters** to see all notes again

### Editing & Deleting Notes
1. In **View All** tab, find your note
2. Click **Edit** to update or **Delete** to remove
3. For edit, click **Save** or **Cancel**

###  View All Tab
- See all notes in chronological order
- **Edit** any note (inline form appears)
- **Delete** notes with confirmation
- Refresh button to reload

###  Search Tab
- **Semantic Search** (default) – Find by meaning
- **Keyword Search** – Find by exact text match
- Relevance scoring for semantic results
- Search via Enter key or button

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/notes` | Create a note |
| GET | `/notes` | List all notes |
| GET | `/notes/{id}` | Get single note |
| PUT | `/notes/{id}` | Edit a note |
| DELETE | `/notes/{id}` | Delete a note |
| GET | `/search?q=...&search_type=...` | Search notes |

### Search Types
- `search_type=semantic` – AI-powered semantic search (default)
- `search_type=keyword` – Simple keyword matching

### Example Requests
```bash
# Create a note
curl -X POST http://127.0.0.1:8000/notes \
  -H "Content-Type: application/json" \
  -d '{"title":"Python Basics","content":"Learn Python fundamentals"}'

# Semantic search
curl "http://127.0.0.1:8000/search?q=machine%20learning&search_type=semantic"

# Keyword search
curl "http://127.0.0.1:8000/search?q=python&search_type=keyword"

# Edit note
curl -X PUT http://127.0.0.1:8000/notes/1 \
  -H "Content-Type: application/json" \
  -d '{"title":"Updated","content":"Updated content"}'

# Delete note
curl -X DELETE http://127.0.0.1:8000/notes/1
```

##  Project Structure

```
app/
  ├── main.py              # FastAPI application & endpoints
  ├── db.py                # SQLite database operations (CRUD)
  ├── embeddings.py        # SentenceTransformers wrapper
  ├── vector_store.py      # Numpy-based semantic search
  ├── notes.db             # SQLite database (auto-created)
  ├── static/
  │   └── index.html       # Web UI (colorful, responsive)
  └── vectors/
      ├── embeddings.npy   # Embedding vectors cache
      └── map.json         # Note ID mappings

requirements.txt           # Python dependencies
README.md                  # This file
```

## 🔧 How It Works

### Creating a Note
1. User fills title & content
2. App creates note in SQLite
3. Text is embedded using SentenceTransformers
4. Embedding is stored in vector store
5. Note ID is mapped to embedding

### Semantic Search
1. User enters query
2. Query is embedded using same model
3. Cosine similarity matches embeddings
4. Results ranked by relevance score
5. Top 5 results returned with % relevance

### Keyword Search
1. User enters keyword
2. Simple substring matching on title & content
3. Results returned in order

##  Dependencies

- **fastapi** – Modern web framework
- **uvicorn** – ASGI server
- **sentence-transformers** – AI embeddings (`all-MiniLM-L6-v2` model)
- **numpy** – Vector operations
- **pydantic** – Data validation
- **python-multipart** – File uploads

##  UI Customization

Edit `app/static/index.html` to customize:
- Colors (currently purple/indigo gradient)
- Fonts and styling
- Button labels and emojis
- Layout and spacing

Edit `app/main.py` to customize:
- Search result limit (default: 5)
- Semantic similarity threshold
- API response formats

##  Using Different Embedding Models

Edit `app/embeddings.py` line 9:

```python
_MODEL = SentenceTransformer("all-mpnet-base-v2")  # Better accuracy
# or
_MODEL = SentenceTransformer("all-MiniLM-L6-v2")   # Faster
```

More models: https://huggingface.co/sentence-transformers

##  Database Schema

```sql
CREATE TABLE notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    content TEXT
)
```

##  Notes

- No authentication required (local use)
- SQLite database stored in `app/notes.db`
- Embeddings cached in `app/vectors/`
- No external API dependencies

##  Deployment

For production, consider:
- Replace SQLite with PostgreSQL
- Add authentication & authorization
- Deploy with Gunicorn/uwsgi
- Use persistent storage for vectors
- Add rate limiting

---

**Enjoy creating and searching notes with AI!** ✨
