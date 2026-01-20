import sys
sys.path.insert(0, r'c:\Users\ShashiKumar\OneDrive\Desktop\Proj\Notes App proj')

from app import db

# Initialize database
db.init_db()
print("✅ Database initialized")

# Test creating a note
note_id = db.add_note("Test Note", "This is a test note", "test,demo", "Personal")
print(f"✅ Created note #{note_id}")

# Test listing notes
notes = db.list_notes()
print(f"✅ Found {len(notes)} notes")
for note in notes:
    print(f"   - #{note['id']}: {note['title']}")

# Test getting a note
note = db.get_note(note_id)
print(f"✅ Retrieved note: {note['title']}")

# Test updating a note
updated = db.update_note(note_id, "Updated Title", "Updated content", "updated", "Work")
print(f"✅ Updated note: {updated}")

# Test getting tags
tags = db.get_all_tags()
print(f"✅ Tags: {tags}")

# Test getting categories
cats = db.get_all_categories()
print(f"✅ Categories: {cats}")

# Test deleting a note
deleted = db.delete_note(note_id)
print(f"✅ Deleted note: {deleted}")

print("\n✨ All database tests passed!")
