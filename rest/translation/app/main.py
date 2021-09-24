import os
import logging
from typing import List

import adaptnlp

import uvicorn
from fastapi import FastAPI

from .data_models import (
    TranslationRequest,
    TranslationResponse,
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
_TRANSLATOR = adaptnlp.EasyTranslator()

# Get Model Configurations From ENV VARS
_TRANSLATION_MODEL = os.environ["TRANSLATION_MODEL"]


# Event Handling
@app.on_event("startup")
async def initialize_nlp_task_modules():
    _TRANSLATOR.translate(
        text="",
        mini_batch_size=1,
        model_name_or_path=_TRANSLATION_MODEL,
        min_length=0,
        max_length=500,
        num_beams=1,
    )


######################
### AdaptNLP API ###
######################
@app.get("/")
async def root():
    return {"message": "Welcome to AdaptNLP"}


@app.post("/api/translator", response_model=TranslationResponse)
async def translator(
    translator_request: TranslationRequest,
):
    text = translator_request.text
    translations = _TRANSLATOR.translate(
        text=text,
        mini_batch_size=1,
        model_name_or_path=_TRANSLATION_MODEL,
        min_length=0,
        max_length=500,
        num_beams=1,
    )
    payload = {"text": translations["translations"]}
    print(payload)
    return payload


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
