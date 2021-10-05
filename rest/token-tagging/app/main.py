import os
import logging
from typing import List

import adaptnlp

import uvicorn
from fastapi import FastAPI

from .data_models import (
    TokenTaggingRequest,
    TokenTaggingResponse,
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
_TOKEN_TAGGER = adaptnlp.EasyTokenTagger()

# Get Model Configurations From ENV VARS
_TOKEN_TAGGING_MODE = os.environ["TOKEN_TAGGING_MODE"]
_TOKEN_TAGGING_MODEL = os.environ["TOKEN_TAGGING_MODEL"]

# Event Handling
@app.on_event("startup")
async def initialize_nlp_task_modules():
    _TOKEN_TAGGER.tag_text(text="", model_name_or_path=_TOKEN_TAGGING_MODEL)


######################
### AdaptNLP API ###
######################
@app.get("/")
async def root():
    return {"message": "Welcome to AdaptNLP"}


@app.post("/api/token_tagger", response_model=List[TokenTaggingResponse])
async def token_tagger(token_tagging_request: TokenTaggingRequest):
    text = token_tagging_request.text
    sentences = _TOKEN_TAGGER.tag_text(
        text=text, model_name_or_path=_TOKEN_TAGGING_MODEL
    )

    # Check if transformers model return type
    if len(sentences) > 0 and isinstance(sentences[0], List):
        payload = [{"text": text, "labels": [], "entities": s} for s in sentences]

        # Need a better way to serialize
        for p in payload:
            entities = p["entities"]
            for e in entities:
                e["text"] = e["word"]
                e["start_pos"] = e["offsets"][0]
                e["end_pos"] = e["offsets"][1]
                e["value"] = e["entity_group"]
                e["confidence"] = e["score"]
        return payload
    
    return payload


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
