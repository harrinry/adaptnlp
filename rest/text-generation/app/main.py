import os
import logging
from typing import List

import adaptnlp

import uvicorn
from fastapi import FastAPI

from .data_models import (
    TextGenerationRequest,
    TextGenerationResponse,
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
_TEXT_GENERATOR = adaptnlp.EasyTextGenerator()

# Get Model Configurations From ENV VARS
_TEXT_GENERATION_MODEL = os.environ["TEXT_GENERATION_MODEL"]


# Event Handling
@app.on_event("startup")
async def initialize_nlp_task_modules():
    _TEXT_GENERATOR.generate(
        text="test",
        mini_batch_size=1,
        model_name_or_path=_TEXT_GENERATION_MODEL,
        num_tokens_to_produce=50,
    )


######################
### AdaptNLP API ###
######################
@app.get("/")
async def root():
    return {"message": "Welcome to AdaptNLP"}


@app.post("/api/text-generator", response_model=TextGenerationResponse)
async def translator(
    text_generator_request: TextGenerationRequest,
):
    text = text_generator_request.text
    num_tokens_to_produce = text_generator_request.num_tokens_to_produce

    generated_text = _TEXT_GENERATOR.generate(
        text=text,
        mini_batch_size=1,
        model_name_or_path=_TEXT_GENERATION_MODEL,
        num_tokens_to_produce=num_tokens_to_produce,
    )
    payload = {"text": generated_text['generated_text']}
    return payload


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
