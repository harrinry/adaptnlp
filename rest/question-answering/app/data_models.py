from typing import List

from pydantic import BaseModel


# QA Label Object
class QASpanLabel(BaseModel):
    text: str
    probability: float


# Question Answering
class QuestionAnsweringRequest(BaseModel):
    query: List[str]
    context: List[str]
    top_n: int = 10


class QuestionAnsweringResponse(BaseModel):
    best_answer: List[str]
    best_n_answers: List[List[QASpanLabel]]
