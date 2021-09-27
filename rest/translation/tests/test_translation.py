import os
os.environ["TRANSLATION_MODEL"] = 'Helsinki-NLP/opus-mt-en-de'

from starlette.testclient import TestClient
from app.main import app


client = TestClient(app)
    
def test_home():
    response = client.get('/')
    assert response.json() == {"message": "Welcome to AdaptNLP"}
    
def test_generation():  
    response = client.post(
        '/api/translator',
    json={"text": ["Including Matt Smith and Leo Decap, this film features a star-studded cast"]},
        headers={"Content-Type":"application/json"}
)
    print(response.json()['text'][0])
    assert response.status_code == 200
    assert response.json()['text'][0] == 'Dieser Film enthält Matt Smith und Leo Decap und zeigt eine starbesetzte Besetzung.'
    
del os.environ["TRANSLATION_MODEL"]