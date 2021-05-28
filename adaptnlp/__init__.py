import pkg_resources
from pathlib import Path

# Easy Modules
from .embeddings import *
from .token_classification import *
from .sequence_classification import *
from .question_answering import *
from .summarization import *
from .translation import *
from .text_generation import *
from .language_model import *
from .model_hub import *

# Training and Fine-tuning Modules
# TODO: Deprecating in 0.3.0+
from .training import SequenceClassifierTrainer
from .transformers.finetuning import LMFineTunerManual

# global variable like flair's: cache_root
cache_root = Path.home()/".adaptnlp"

__version__ = "0.2.3"

__all__ = [
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
