import os
os.environ["TOKEN_TAGGING_MODE"] = 'ner'
os.environ["TOKEN_TAGGING_MODEL"] = 'ner-ontonotes-fast'

from starlette.testclient import TestClient
from app.main import app


client = TestClient(app)
    
def test_home():
    response = client.get('/')
    assert response.json() == {"message": "Welcome to AdaptNLP"}
    
def test_generation():  
    response = client.post(
        '/api/token_tagger',
    json={"text": "Hello World, my name is Will Smith and I fight aliens"},
        headers={"Content-Type":"application/json"}
)
    assert response.status_code == 200
    assert response.json()[0]['entities'][0]['text'] == 'Will Smith'
    assert response.json()[0]['entities'][0]['value'] == 'PERSON'
    
del os.environ["TOKEN_TAGGING_MODE"]
del os.environ["TOKEN_TAGGING_MODEL"]