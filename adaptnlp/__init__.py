__version__ = "0.3.0"

from pathlib import Path

# global variable like Flair's cache_root
cache_root = Path.home()/".adaptnlp"

# Inference modules
from .inference.embeddings import (
    EasyWordEmbeddings,
    EasyStackedEmbeddings,
    EasyDocumentEmbeddings
)

from .inference.sequence_classification import (
    EasySequenceClassifier,
    TransformersSequenceClassifier,
    FlairSequenceClassifier
)

from .inference.token_classification import EasyTokenTagger
from .inference.question_answering import EasyQuestionAnswering, TransformersQuestionAnswering
from .inference.summarization import EasySummarizer, TransformersSummarizer
from .inference.translation import EasyTranslator, TransformersTranslator
from .inference.text_generation import EasyTextGenerator, TransformersTextGenerator

from .result import DetailLevel

# Huggingface Hub bits
from .model_hub import HFModelHub, FlairModelHub, HF_TASKS, FLAIR_TASKS

# Training API
from .training.core import Strategy, TaskDatasets, AdaptiveTuner
from .training.sequence_classification import SequenceClassificationTuner, SequenceClassificationDatasets
from .training.language_model import LanguageModelTuner, LanguageModelDatasets


__all__ = [
    "__version__",
    "EasyWordEmbeddings",
    "EasyStackedEmbeddings",
    "EasyDocumentEmbeddings",
    "EasySequenceClassifier",
    "TransformersSequenceClassifier",
    "FlairSequenceClassifier",
    "EasyTokenTagger",
    "EasyQuestionAnswering",
    "TransformersQuestionAnswering",
    "EasySummarizer",
    "TransformersSummarizer",
    "EasyTranslator",
    "TransformersTranslator",
    "EasyTextGenerator",
    "TransformersTextGenerator",
    "DetailLevel",
    "HFModelHub",
    "FlairModelHub",
    "HF_TASKS",
    "FLAIR_TASKS",
    "TaskDatasets",
    "AdaptiveTuner",
    "Strategy",
    "SequenceClassificationDatasets",
    "LanguageModelDatasets",
    "SequenceClassificationTuner",
    "LanguageModelTuner"
]