import os
os.environ["TOKEN_TAGGING_MODE"] = 'ner'
os.environ["TOKEN_TAGGING_MODEL"] = 'flair/ner-english-ontonotes'

from starlette.testclient import TestClient
from app.main import app


client = TestClient(app)
    
def test_home():
    response = client.get('/')
    assert response.json() == {"message": "Welcome to AdaptNLP"}
    
def test_generation():  
    response = client.post(
        '/api/token_tagger',
    json={"text": ["Jack walked through the park on a Sunday.","Now this is Will's second sentence"]},
        headers={"Content-Type":"application/json"}
)
    assert response.status_code == 200
    assert response.json()[0]['entities'][0]['text'] == 'Jack'
    assert response.json()[0]['entities'][0]['value'] == 'PERSON'
    assert response.json()[0]['entities'][1]['text'] == 'Sunday'
    assert response.json()[0]['entities'][1]['value'] == 'DATE'
    assert response.json()[1]['entities'][0]['text'] == 'Will'
    assert response.json()[1]['entities'][0]['value'] == 'PERSON'
    
del os.environ["TOKEN_TAGGING_MODE"]
del os.environ["TOKEN_TAGGING_MODEL"]