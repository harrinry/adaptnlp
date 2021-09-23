import os
import logging
from typing import List

import adaptnlp

import uvicorn
from fastapi import FastAPI

from .data_models import (
    SequenceClassificationRequest,
    SequenceClassificationResponse,
)

app = FastAPI()

#####################
### Initialization###
#####################

# Initialize Logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level="INFO",
    format="%(process)d-%(levelname)s-%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Global Modules
_SEQUENCE_CLASSIFIER = adaptnlp.EasySequenceClassifier()

# Get Model Configurations From ENV VARS
_SEQUENCE_CLASSIFICATION_MODEL = os.environ["SEQUENCE_CLASSIFICATION_MODEL"]


# Event Handling
@app.on_event("startup")
async def initialize_nlp_task_modules():
    _SEQUENCE_CLASSIFIER.tag_text(
        text="test_me", mini_batch_size=1, model_name_or_path=_SEQUENCE_CLASSIFICATION_MODEL
    )


######################
### AdaptNLP API ###
######################
@app.get("/")
async def root():
    return {"message": "Welcome to AdaptNLP"}


@app.post(
    "/api/sequence-classifier", response_model=List[SequenceClassificationResponse]
)
async def sequence_classifier(
    sequence_classification_request: SequenceClassificationRequest,
):
    text = sequence_classification_request.text
    sentences = _SEQUENCE_CLASSIFIER.tag_text(
        text=text, mini_batch_size=1, model_name_or_path=_SEQUENCE_CLASSIFICATION_MODEL,detail_level="low"
    )
    response = []
    curr_d = {}
    for i in range(len(sentences["sentences"])):
        curr_d["text"] = sentences["sentences"][i]
        curr_d["probability"] = sentences["probs"][i].tolist()
        curr_d["prediction"] = sentences["predictions"][i]
        response.append(curr_d)
        curr_d = {}
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
