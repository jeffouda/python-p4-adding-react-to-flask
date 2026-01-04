
import pytest
from app import app, db
from models import Message

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

def test_codegrade_placeholder():
    """Codegrade placeholder test"""
    assert 1==1

def test_get_messages(client):
    """Test GET /messages returns empty list initially"""
    response = client.get('/messages')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 0

def test_post_message(client):
    """Test POST /messages creates a new message"""
    response = client.post('/messages', json={'body': 'Hello', 'username': 'Alice'})
    assert response.status_code == 201
    data = response.get_json()
    assert data['body'] == 'Hello'
    assert data['username'] == 'Alice'
    assert 'id' in data
    assert 'created_at' in data

def test_get_messages_after_post(client):
    """Test GET /messages returns messages after posting"""
    client.post('/messages', json={'body': 'Hello', 'username': 'Alice'})
    client.post('/messages', json={'body': 'Hi', 'username': 'Bob'})
    response = client.get('/messages')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2
    assert data[0]['body'] == 'Hello'
    assert data[1]['body'] == 'Hi'

def test_patch_message(client):
    """Test PATCH /messages/<id> updates a message"""
    post_response = client.post('/messages', json={'body': 'Hello', 'username': 'Alice'})
    message_id = post_response.get_json()['id']
    response = client.patch(f'/messages/{message_id}', json={'body': 'Updated Hello'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['body'] == 'Updated Hello'
    assert data['username'] == 'Alice'

def test_delete_message(client):
    """Test DELETE /messages/<id> deletes a message"""
    post_response = client.post('/messages', json={'body': 'Hello', 'username': 'Alice'})
    message_id = post_response.get_json()['id']
    response = client.delete(f'/messages/{message_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['deleted'] == True
    # Check it's deleted
    get_response = client.get('/messages')
    assert len(get_response.get_json()) == 0