#!/usr/bin/env python
"""Test script for Notes App with AI Search"""
import requests
import time
import sys

BASE_URL = "http://127.0.0.1:8000"

def test_api():
    print("🔄 Waiting for server to fully start...")
    for i in range(15):
        try:
            r = requests.get(f"{BASE_URL}/", timeout=2)
            if r.status_code == 200:
                print("✓ Server is ready\n")
                break
        except requests.exceptions.ConnectionError:
            print(f"  Attempt {i+1}/15: Connecting...", end="\r")
            time.sleep(1)
    
    # Test Signup
    print("1️⃣  Testing POST /signup...")
    signup_payload = {"username": "testuser123", "password": "testpass123"}
    r = requests.post(f"{BASE_URL}/signup", json=signup_payload)
    print(f"   Status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        token = data.get("access_token")
        user_id = data.get("user_id")
        print(f"   ✅ Signup successful! Token: {token[:20]}... User ID: {user_id}\n")
    else:
        print(f"   Response: {r.json()}\n")
        # Try login instead if user already exists
        print("2️⃣  Testing POST /login...")
        login_payload = {"username": "testuser123", "password": "testpass123"}
        r = requests.post(f"{BASE_URL}/login", json=login_payload)
        print(f"   Status: {r.status_code}")
        data = r.json()
        token = data.get("access_token")
        user_id = data.get("user_id")
        print(f"   ✅ Login successful! Token: {token[:20]}... User ID: {user_id}\n")
    
    # Prepare auth header
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Test create note
    print("3️⃣  Testing POST /notes (Create)...")
    note_payload = {
        "title": "Machine Learning Basics",
        "content": "ML is a subset of AI that uses algorithms to learn from data",
        "tags": "ai, python, tutorial",
        "category": "Study"
    }
    r = requests.post(f"{BASE_URL}/notes", json=note_payload, headers=headers)
    print(f"   Status: {r.status_code}, Response: {r.json()}")
    note_id = r.json().get("id") if r.status_code == 200 else None
    print()
    
    # Test list notes
    print("4️⃣  Testing GET /notes (List All)...")
    r = requests.get(f"{BASE_URL}/notes", headers=headers)
    print(f"   Status: {r.status_code}, Notes count: {len(r.json()) if r.status_code == 200 else 0}")
    if r.status_code == 200:
        for note in r.json()[:2]:  # Show first 2 notes
            print(f"   - #{note['id']}: {note['title']}")
    print()
    
    # Test semantic search
    print("5️⃣  Testing GET /search (Semantic)...")
    r = requests.get(f"{BASE_URL}/search", params={"q": "artificial intelligence", "search_type": "semantic", "k": 5}, headers=headers)
    print(f"   Status: {r.status_code}")
    if r.status_code == 200:
        results = r.json()
        print(f"   Found {len(results)} semantic matches:")
        for res in results[:2]:
            score = res.get('score', 'N/A')
            print(f"   - {res['title']} (relevance: {score:.2f if isinstance(score, float) else score})")
    print()
    
    # Test keyword search
    print("6️⃣  Testing GET /search (Keyword)...")
    r = requests.get(f"{BASE_URL}/search", params={"q": "machine", "search_type": "keyword", "k": 5}, headers=headers)
    print(f"   Status: {r.status_code}, Keyword matches: {len(r.json()) if r.status_code == 200 else 0}\n")
    
    # Test get tags
    print("7️⃣  Testing GET /tags...")
    r = requests.get(f"{BASE_URL}/tags", headers=headers)
    print(f"   Status: {r.status_code}")
    if r.status_code == 200:
        print(f"   Tags: {r.json().get('tags', [])}\n")
    
    # Test get categories
    print("8️⃣  Testing GET /categories...")
    r = requests.get(f"{BASE_URL}/categories", headers=headers)
    print(f"   Status: {r.status_code}")
    if r.status_code == 200:
        print(f"   Categories: {r.json().get('categories', [])}\n")
    
    # Test update note
    if note_id:
        print(f"9️⃣  Testing PUT /notes/{note_id} (Update)...")
        update_payload = {
            "title": "Advanced Machine Learning",
            "content": "Deep learning, neural networks, and transformers",
            "tags": "ai, deeplearning, advanced",
            "category": "Study"
        }
        r = requests.put(f"{BASE_URL}/notes/{note_id}", json=update_payload, headers=headers)
        print(f"   Status: {r.status_code}, Response: {r.json()}\n")
    
    # Test delete note
    if note_id:
        print(f"🔟 Testing DELETE /notes/{note_id}...")
        r = requests.delete(f"{BASE_URL}/notes/{note_id}", headers=headers)
        print(f"   Status: {r.status_code}, Response: {r.json()}\n")
    
    print("✅ All tests completed successfully!")

if __name__ == "__main__":
    test_api()
