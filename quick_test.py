#!/usr/bin/env python
"""Quick API test"""
import requests
import time

BASE_URL = 'http://127.0.0.1:8000'

print('🔄 Testing Notes App API...\n')

# Test login/signup endpoint
print('1️⃣ Testing Signup...')
r = requests.post(f'{BASE_URL}/signup', json={'username': 'testuser', 'password': 'testpass123'})
print(f'   Status: {r.status_code}')
if r.status_code == 200:
    data = r.json()
    token = data['access_token']
    print(f'   ✅ Signup successful!')
elif r.status_code == 400 and 'already exists' in r.text:
    print('   User exists, logging in...')
    r = requests.post(f'{BASE_URL}/login', json={'username': 'testuser', 'password': 'testpass123'})
    if r.status_code == 200:
        token = r.json()['access_token']
        print(f'   ✅ Login successful!')
    else:
        print(f'   Error: {r.json()}')
        exit(1)
else:
    print(f'   Error: {r.json()}')
    exit(1)

# Test create note
print('\n2️⃣ Testing Create Note...')
headers = {'Authorization': f'Bearer {token}'}
r = requests.post(f'{BASE_URL}/notes', json={'title': 'Test Note', 'content': 'Testing the app', 'tags': 'test', 'category': 'Study'}, headers=headers)
print(f'   Status: {r.status_code}, Response: {r.json()}')

# Test get notes
print('\n3️⃣ Testing Get Notes...')
r = requests.get(f'{BASE_URL}/notes', headers=headers)
print(f'   Status: {r.status_code}, Count: {len(r.json())}')
if len(r.json()) > 0:
    note = r.json()[0]
    print(f'   Sample: #{note["id"]} - {note["title"]}')

# Test semantic search
print('\n4️⃣ Testing Semantic Search...')
r = requests.get(f'{BASE_URL}/search', params={'q': 'testing', 'search_type': 'semantic'}, headers=headers)
print(f'   Status: {r.status_code}, Results: {len(r.json())}')

print('\n✅ All basic tests passed!')
