import os
os.environ["SUMMARIZATION_MODEL"] = 'facebook/bart-large-cnn'

from starlette.testclient import TestClient
from app.main import app


client = TestClient(app)
    
def test_home():
    response = client.get('/')
    assert response.json() == {"message": "Welcome to AdaptNLP"}
    
def test_summarization():  
    response = client.post(
        '/api/summarizer',
    json={"min_length":"100", "max_length":"500","text":["Einstein’s education was disrupted by his father’s repeated failures at business. In 1894, after his company failed to get an important contract to electrify the city of Munich, Hermann Einstein moved to Milan to work with a relative. Einstein was left at a boardinghouse in Munich and expected to finish his education. Alone, miserable, and repelled by the looming prospect of military duty when he turned 16, Einstein ran away six months later and landed on the doorstep of his surprised parents. His parents realized the enormous problems that he faced as a school dropout and draft dodger with no employable skills. His prospects did not look promising. Fortunately, Einstein could apply directly to the Eidgenössische Polytechnische Schule (“Swiss Federal Polytechnic School”; in 1911, following expansion in 1909 to full university status, it was renamed the Eidgenössische Technische Hochschule, or “Swiss Federal Institute of Technology”) in Zürich without the equivalent of a high school diploma if he passed its stiff entrance examinations. His marks  showed that he excelled in mathematics and physics, but he failed at French, chemistry, and biology. Because of his exceptional math scores, he was allowed into the polytechnic on the condition that he first finish his formal schooling. He went to a special high school run by Jost Winteler in Aarau, Switzerland, and graduated in 1896. He also renounced his German citizenship at that time. (He was stateless until 1901, when he was granted Swiss citizenship.) He became lifelong friends with the Winteler family, with whom he had been boarding. (Winteler’s daughter, Marie, was Einstein’s first love; Einstein’s sister, Maja, would eventually marry Winteler’s son Paul; and his close friend Michele Besso would marry their eldest daughter, Anna.)"]},
        headers={"Content-Type":"application/json"}
)
    assert response.status_code == 200
    assert response.json()['text'][0] == "Einstein’s education was disrupted by his father's repeated failures at business. In 1894, after his company failed to get an important contract to electrify the city of Munich, Hermann Einstein moved to Milan to work with a relative. Einstein was left at a boardinghouse in Munich and expected to finish his education. Because of his exceptional math scores, he was allowed into the polytechnic on the condition that he first finish his formal schooling. He went to a special high school run by Jost Winteler in Aarau, Switzerland and graduated in 1896."
    
del os.environ["SUMMARIZATION_MODEL"]