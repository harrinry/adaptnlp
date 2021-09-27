import os
os.environ["TEXT_GENERATION_MODEL"] = 'gpt2'

from starlette.testclient import TestClient
from app.main import app


client = TestClient(app)
    
def test_home():
    response = client.get('/')
    assert response.json() == {"message": "Welcome to AdaptNLP"}
    
def test_generation():  
    response = client.post(
        '/api/text-generator',
    json={"num_tokens_to_produce":"50", "text": "Portrayed by Matt Smith,"},
        headers={"Content-Type":"application/json"}
)
    assert response.status_code == 200
    assert response.json()['text'][0] == 'Portrayed by Matt Smith, the film is a bit of a departure from the usual "I\'m not a fan of the show" type of film. It\'s a bit of a departure from the usual "I\'m not a fan of the show" type of film. It'
    
del os.environ["TEXT_GENERATION_MODEL"]