import os
import logging
from typing import List

import adaptnlp

import uvicorn
from fastapi import FastAPI

from .data_models import (
    SummarizationRequest,
    SummarizationResponse,
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
_SUMMARIZER = adaptnlp.EasySummarizer()

# Get Model Configurations From ENV VARS
_SUMMARIZATION_MODEL = os.environ["SUMMARIZATION_MODEL"]


# Event Handling
@app.on_event("startup")
async def initialize_nlp_task_modules():
    _SUMMARIZER.summarize(
        text="",
        mini_batch_size=1,
        model_name_or_path=_SUMMARIZATION_MODEL,
        min_length=0,
        max_length=500,
        num_beams=4,
        early_stopping=True,
    )

######################
### AdaptNLP API ###
######################
@app.get("/")
async def root():
    return {"message": "Welcome to AdaptNLP"}


@app.post("/api/summarizer", response_model=SummarizationResponse)
async def translator(
    summarizer_request: SummarizationRequest,
):
    text = summarizer_request.text
    min_length = summarizer_request.min_length
    max_length = summarizer_request.max_length

    summaries = _SUMMARIZER.summarize(
        text=text,
        mini_batch_size=1,
        model_name_or_path=_SUMMARIZATION_MODEL,
        min_length=min_length,
        max_length=max_length,
        num_beams=4,
    )
    payload = {"text": summaries["summaries"]}
    return payload


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
