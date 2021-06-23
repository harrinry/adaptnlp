__version__ = "0.2.3"

import pkg_resources
from pathlib import Path

# Easy Modules
from .embeddings import (
    EasyWordEmbeddings,
    EasyStackedEmbeddings,
    EasyDocumentEmbeddings,
)
from .token_classification import EasyTokenTagger
from .sequence_classification import (
    EasySequenceClassifier,
    TransformersSequenceClassifier,
    FlairSequenceClassifier,
)
from .question_answering import EasyQuestionAnswering, TransformersQuestionAnswering
from .summarization import EasySummarizer, TransformersSummarizer
from .translation import EasyTranslator, TransformersTranslator
from .text_generation import EasyTextGenerator, TransformersTextGenerator


# global variable like flair's: cache_root
cache_root = Path.home()/".adaptnlp"


__all__ = [
    "__version__",
    "EasyWordEmbeddings",
    "EasyStackedEmbeddings",
    "EasyDocumentEmbeddings",
    "EasyTokenTagger",
    "EasySequenceClassifier",
    "FlairSequenceClassifier",
    "TransformersSequenceClassifier",
    "EasyQuestionAnswering",
    "TransformersQuestionAnswering",
    "EasySummarizer",
    "TransformersSummarizer",
    "EasyTranslator",
    "TransformersTranslator",
    "EasyTextGenerator",
    "TransformersTextGenerator",
    "SequenceClassifierTrainer",
    "LMFineTuner",
    "LMFineTunerManual",
]