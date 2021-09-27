from starlette.testclient import TestClient
import os

from app.main import app

os.environ["QUESTION_ANSWERING_MODEL"] = 'distilbert-base-uncased-distilled-squad'

client = TestClient(app)
    
def test_home():
    response = client.get('/')
    assert response.json() == {"message": "Welcome to AdaptNLP"}
    
def test_qa():
    response = client.post(
        '/api/question-answering',
    json={"query": ["When did AdaptNLP release?"], "context": ["Released in 2018, AdaptNLP was at the forefront of simplistic inference API with Transformers and Flair"], "top_n":"5"},
        headers={"Content-Type":"application/json"}
)
    assert response.status_code == 200
    assert response.json()['best_answer'] == ['2018']
    
del os.environ["QUESTION_ANSWERING_MODEL"]