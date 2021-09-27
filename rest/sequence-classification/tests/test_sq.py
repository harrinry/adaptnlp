import os
os.environ["SEQUENCE_CLASSIFICATION_MODEL"] = 'en-sentiment'

from starlette.testclient import TestClient
from app.main import app


client = TestClient(app)
    
def test_home():
    response = client.get('/')
    assert response.json() == {"message": "Welcome to AdaptNLP"}
    
def test_qa():  
    response = client.post(
        '/api/sequence-classifier',
    json={"text": "Matt Damon is a horrible actor"},
        headers={"Content-Type":"application/json"}
)
    assert response.status_code == 200
    assert response.json()[0]['prediction'] == 'NEGATIVE'
    
del os.environ["SEQUENCE_CLASSIFICATION_MODEL"]