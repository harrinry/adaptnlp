from typing import List, Tuple

from pydantic import BaseModel


# General Data Models
class Labels(BaseModel):
    predictions: str
    probabilities: float
    

# Sequence Classification
class SequenceClassificationRequest(BaseModel):
    text: str


class SequenceClassificationResponse(BaseModel):
    text: str
    probability: Tuple[float]
    prediction: str
        
### We get back:

# Sentences
# Predictions
# Probabilities
# Pairings
# Classes