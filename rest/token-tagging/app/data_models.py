from typing import List

from pydantic import BaseModel


# General Data Models
class Labels(BaseModel):
    value: str
    confidence: float


class Entities(BaseModel):
    text: str
    start_pos: int
    end_pos: int
    value: str
    confidence: float


# Token Tagging Data Model
class TokenTaggingRequest(BaseModel):
    text: List[str]


class TokenTaggingResponse(BaseModel):
    text: str
    labels: List[Labels] = []
    entities: List[Entities] = []
