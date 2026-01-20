# 🚀 Quick Start Guide - AI Enhanced Notes App

## Installation & Setup

### Step 1: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 2: Start the Server
```powershell
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

You should see:
```
INFO:     Started server process [XXXX]
INFO:     Waiting for application startup.
(SentenceTransformers model downloads and initializes...)
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

### Step 3: Open the App
Visit **http://127.0.0.1:8000** in your web browser

## User Interface

### 📝 Create Tab
1. Enter note title
2. Enter note content
3. (Optional) Select a category
4. (Optional) Add comma-separated tags
5. Click "✨ Add Note"

### 📋 View All Tab
1. See all your notes
2. Use filter buttons for tags and categories
3. Click "✏️ Edit" to modify a note
4. Click "🗑️ Delete" to remove a note
5. Click "🔄 Refresh Notes" to reload

### 🔍 Search Tab
1. Choose search type:
   - 🤖 Semantic (AI-powered by meaning) ← **Recommended**
   - 🔤 Keyword (exact text match)
2. Type your query
3. Press Enter or click "🔍 Search"
4. See results with relevance scores

## Features Explained

### 🤖 Semantic Search
- Uses AI to understand *meaning* not just keywords
- Example: Search "productivity tips" finds notes about "time management" and "focus"
- Shows relevance scores:
  - 🔥 > 70% = Hot match
  - ⭐ 50-70% = Good match
  - 💡 < 50% = Relevant match

### 📁 Organization
- **Tags**: Add multiple comma-separated tags per note
  - Search and filter by specific tags
  - Example: `python, tutorial, beginner`
- **Categories**: One category per note
  - Predefined: Personal, Work, Study, Ideas, Tasks
  - Filter all notes by category

### 🔐 Security
- Passwords are hashed with bcrypt
- Each user has isolated, private notes
- JWT tokens expire after 7 days
- Token stored securely in browser localStorage

## Testing

### Quick API Test
```powershell
python test_app.py
```

This will:
1. ✅ Create a test user (or login if exists)
2. ✅ Create a sample note
3. ✅ List all notes
4. ✅ Test semantic search
5. ✅ Test keyword search
6. ✅ Test tags and categories
7. ✅ Update the note
8. ✅ Delete the note

## Common Tasks

### Create Multiple Notes
1. Go to "Create" tab
2. Enter details and click "Add Note"
3. Form resets automatically
4. Repeat as needed

### Search for a Concept
1. Go to "Search" tab
2. Select "🤖 Semantic"
3. Type what you're looking for, not exact text
4. Get results by meaning

### Organize with Tags
1. Create a note with tags: `python, tips, functions`
2. Go to "View All" tab
3. Click "python" tag filter button
4. See all notes with that tag

### Logout Safely
1. Click "Logout" button (top right)
2. Returns to login page
3. Your notes are saved

## File Structure

```
Notes App proj/
├── app/
│   ├── main.py              # FastAPI app & endpoints
│   ├── db.py                # SQLite database functions
│   ├── auth.py              # JWT & password hashing
│   ├── embeddings.py        # SentenceTransformers
│   ├── vector_store.py      # Vector search & storage
│   ├── notes.db             # SQLite database file
│   ├── static/
│   │   ├── index.html       # Main app interface
│   │   ├── login.html       # Auth interface
│   ├── vectors/
│   │   ├── embeddings.npy   # Vector embeddings
│   │   ├── map.json         # Note ID mapping
│   └── __pycache__/
├── requirements.txt         # Python dependencies
├── test_app.py             # Comprehensive test suite
├── quick_test.py           # Simple API test
└── README.md               # Full documentation
```

## Troubleshooting

### "Connection refused" error
- Make sure the server is running: `uvicorn app.main:app --host 127.0.0.1 --port 8000`
- Check it's on http://127.0.0.1:8000 (not localhost:8000)

### "Invalid token" on page refresh
- Tokens are stored in localStorage
- Clear cache and login again if issues persist
- Log out and log back in

### "Model download slow"
- First startup downloads the AI model (~90MB)
- This is normal, happens once per machine
- Check your internet connection

### Search returns no results
- Try the 🔤 Keyword search first
- Make sure the note content contains related words
- Use more general terms for semantic search

### Tags not appearing
- Make sure you added tags when creating the note
- Use comma-separated values: `tag1, tag2, tag3`
- Spaces are trimmed automatically

## API Examples (Advanced)

### Create Note with curl
```bash
curl -X POST http://127.0.0.1:8000/notes \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Python Tips",
    "content": "Use list comprehensions for efficiency",
    "tags": "python, performance",
    "category": "Study"
  }'
```

### Search with curl
```bash
curl "http://127.0.0.1:8000/search?q=machine%20learning&search_type=semantic" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Pro Tips

1. **Use descriptive titles**: Better for both search types
2. **Be specific with content**: Semantic search works better with detailed notes
3. **Organize with categories**: Faster filtering than scrolling
4. **Use meaningful tags**: Think of tags as note topics
5. **Search by concept**: Try "problems with X" or "how to Y" in semantic search
6. **Regular backups**: Database is in `app/notes.db`, backup periodically

## Performance Notes

- Semantic search is powered by embeddings (takes ~100ms)
- Keyword search is instant (indexed lookup)
- Vector embeddings are cached after first creation
- First app startup takes longer (model download + initialization)
- Subsequent startups are instant

---

**Version**: 1.0.0  
**Status**: ✅ Production Ready  
**Last Updated**: January 19, 2026
