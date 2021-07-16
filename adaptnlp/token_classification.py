# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/05_token_classification.ipynb (unless otherwise specified).

__all__ = ['logger', 'TransformersTokenTagger', 'FlairTokenTagger', 'EasyTokenTagger']

# Cell
import logging
from typing import List, Dict, Union
from collections import defaultdict

import numpy as np

import torch
from torch.utils.data import TensorDataset

from flair.data import Sentence
from flair.models import SequenceTagger
from transformers import (
    AutoTokenizer,
    AutoModelForTokenClassification,
    PreTrainedTokenizer,
    PreTrainedModel,
    BertForSequenceClassification,
    XLNetForSequenceClassification,
    AlbertForSequenceClassification,
)

from .model import AdaptiveModel, DataLoader
from .model_hub import HFModelResult, FlairModelResult, FlairModelHub, HFModelHub

from fastai_minima.utils import to_detach, apply, to_device

from fastcore.basics import Self, risinstance
from fastcore.xtras import Path

# Cell
logger = logging.getLogger(__name__)

# Cell
class TransformersTokenTagger(AdaptiveModel):
    "Adaptive model for Transformer's Token Tagger Model"
    def __init__(
        self,
        tokenizer: PreTrainedTokenizer, # A tokenizer object from Huggingface's transformers (TODO) and tokenizers
        model: PreTrainedModel # A transformers token tagger model
    ):
        # Load up model and tokenizer
        self.tokenizer = tokenizer
        super().__init__()

        # Sets the internal model
        self.set_model(model)

    @classmethod
    def load(
        cls,
        model_name_or_path: str # A key string of one of Transformer's pre-trained Token Tagger Model or a `HFModelResult`
    ) -> AdaptiveModel:
        "Class method for loading and constructing this tagger"
        if isinstance(model_name_or_path, HFModelResult): model_name_or_path = model_name_or_path.name
        tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
        model = AutoModelForTokenClassification.from_pretrained(model_name_or_path)
        tagger = cls(tokenizer, model)
        return tagger

    def predict(
        self,
        text: Union[List[str], str], # String, list of strings, sentences, or list of sentences to run inference on
        mini_batch_size: int = 32, # Mini batch size
        grouped_entities: bool = True, # Set True to get whole entity span strings (Default True)
        **kwargs, # Optional arguments for the Transformers tagger
    ) -> List[List[Dict]]:
        """Predict method for running inference using the pre-trained token tagger model.

        **Returns**:
        A list of lists of tagged entities.
        """
        if isinstance(text, str):
            text = [text]
        results: List[Dict] = []

        dataset = self._tokenize(text)
        dl = DataLoader(dataset, batch_size=mini_batch_size)

        logger.info(f'Running prediction on {len(dataset)} text sequences')
        logger.info(f'Batch size = {mini_batch_size}')

        outputs,_ = super().get_preds(dl=dl)

        inputs = apply(to_device, [b for b in dl], device='cpu')
        inputs = torch.cat(*inputs)
        inputs = apply(Self.numpy(), inputs)

        outputs = torch.cat([o['logits'] for o in outputs])
        outputs = apply(to_detach, outputs, cpu=True)
        outputs = apply(Self.numpy(), outputs)

        # Iterate through batch for tagged token predictions
        for idx, pred in enumerate(outputs):
            entities = pred
            input_ids = inputs[idx]
            tagged_entities = self._generate_tagged_entities(
                entities=entities,
                input_ids=input_ids,
                grouped_entities=grouped_entities
            )
            results += tagged_entities

        return results

    def _tokenize(
        self, sentences: Union[List[Sentence], Sentence, List[str], str]
    ) -> TensorDataset:
        """ Batch tokenizes text and produces a `TensorDataset` with them """

        tokenized_text = self.tokenizer.batch_encode_plus(
            sentences,
            return_tensors="pt",
            pad_to_max_length=True,
        )

        # Bart, XLM, DistilBERT, RoBERTa, and XLM-RoBERTa don't use token_type_ids
        if isinstance(
            self.model,
            (
                BertForSequenceClassification,
                XLNetForSequenceClassification,
                AlbertForSequenceClassification,
            ),
        ):
            dataset = TensorDataset(
                tokenized_text["input_ids"],
                tokenized_text["attention_mask"],
                tokenized_text["token_type_ids"],
            )
        else:
            dataset = TensorDataset(
                tokenized_text["input_ids"], tokenized_text["attention_mask"]
            )

        return dataset

    # `_group_entites` and `_generate_tagged_entities` modified from pipeline code snippet from Transformers
    def _group_entities(
        self, entities: List[dict], idx_start: int, idx_end: int
    ) -> Dict:
        """Returns grouped entities"""
        # Get the last entity in the entity group
        entity = entities[-1]["entity"]
        scores = np.mean([entity["score"] for entity in entities])
        tokens = [entity["word"] for entity in entities]

        entity_group = {
            "entity_group": entity,
            "score": np.mean(scores),
            "word": self.tokenizer.convert_tokens_to_string(tokens),
            "offsets": (idx_start, idx_end),
        }
        return entity_group

    def _generate_tagged_entities(
        self, entities: np.ndarray, input_ids: np.ndarray, grouped_entities: bool = True
    ) -> List[Dict]:
        """Generate full list of entities given tagged token predictions and input_ids"""

        score = np.exp(entities) / np.exp(entities).sum(-1, keepdims=True)
        labels_idx = score.argmax(axis=-1)

        answers = []
        entities = []
        entity_groups = []
        entity_group_disagg = []
        # Filter to labels not in `self.ignore_labels`
        filtered_labels_idx = [
            (idx, label_idx)
            for idx, label_idx in enumerate(labels_idx)
            if self.model.config.id2label[label_idx] not in ["O"]
        ]

        for idx, label_idx in filtered_labels_idx:
            # print(tokenizer.convert_ids_to_tokens(int(input_ids[idx])))
            entity = {
                "word": self.tokenizer.convert_ids_to_tokens(int(input_ids[idx])),
                "score": score[idx][label_idx].item(),
                "entity": self.model.config.id2label[label_idx],
                "index": idx,
            }
            last_idx, _ = filtered_labels_idx[-1]
            if grouped_entities:
                if not entity_group_disagg:
                    entity_group_disagg += [entity]
                    if idx == last_idx:
                        entity_groups += [
                            self._group_entities(
                                entity_group_disagg, idx - len(entity_group_disagg), idx
                            )
                        ]
                    continue

                # If the current entity is similar and adjacent to the previous entity, append it to the disaggregated entity group
                if (
                    entity["entity"] == entity_group_disagg[-1]["entity"]
                    and entity["index"] == entity_group_disagg[-1]["index"] + 1
                ):
                    entity_group_disagg += [entity]
                    # Group the entities at the last entity
                    if idx == last_idx:
                        entity_groups += [
                            self._group_entities(
                                entity_group_disagg, idx - len(entity_group_disagg), idx
                            )
                        ]
                # If the current entity is different from the previous entity, aggregate the disaggregated entity group
                else:
                    entity_groups += [
                        self._group_entities(
                            entity_group_disagg,
                            entity_group_disagg[-1]["index"] - len(entity_group_disagg),
                            entity_group_disagg[-1]["index"],
                        )
                    ]
                    entity_group_disagg = [entity]

            entities += [entity]

        # Append
        if grouped_entities:
            answers += [entity_groups]
        else:
            answers += [entities]

        return answers

    def train(
        self,
    ):
        raise NotImplementedError

    def evaluate(
        self,
    ):
        raise NotImplementedError

# Cell
class FlairTokenTagger(AdaptiveModel):
    """Adaptive Model for Flair's Token Tagger

    To find a list of available models, see [here](https://huggingface.co/models?filter=flair)
    """

    def __init__(
        self,
        model_name_or_path: str # A key string of one of Flair's pre-trained Token tagger Model
    ):
        self.tagger = SequenceTagger.load(model_name_or_path)

    @classmethod
    def load(
        cls,
        model_name_or_path: str # A key string of one of Flair's pre-trained Token tagger Model
    ) -> AdaptiveModel:
        "Class method for loading a constructing this tagger"
        tagger = cls(model_name_or_path)
        return tagger

    def predict(
        self,
        text: Union[List[Sentence], Sentence, List[str], str], # String, list of strings, sentences, or list of sentences to run inference on
        mini_batch_size: int = 32, # Mini batch size
        **kwargs, # Optional arguments for the Flair tagger
    ) -> List[Sentence]:
        "Predict method for running inference using the pre-trained token tagger model"

        if isinstance(text, (Sentence, str)):
            text = [text]
        if isinstance(text[0], str):
            text = [Sentence(s) for s in text]
        self.tagger.predict(
            sentences=text,
            mini_batch_size=mini_batch_size,
            **kwargs,
        )
        return text

    def train(
        self,
    ):
        raise NotImplementedError

    def evaluate(
        self,
    ):

        raise NotImplementedError

# Cell
class EasyTokenTagger:
    "Token level classification models"

    def __init__(self):
        self.token_taggers: Dict[AdaptiveModel] = defaultdict(bool)

    def tag_text(
        self,
        text: Union[List[Sentence], Sentence, List[str], str], # Text input, it can be a string or any of Flair's `Sentence` input formats
        model_name_or_path: Union[str, FlairModelResult, HFModelResult] = "ner-ontonotes", # The hosted model name key or model path
        mini_batch_size: int = 32, # The mini batch size for running inference
        **kwargs, # Keyword arguments for Flair's `SequenceTagger.predict()` method
    ) -> List[Sentence]:
        """Tags tokens with labels the token classification models have been trained on

        **Returns**: A list of Flair's `Sentence`'s
        """
        # Load Sequence Tagger Model and Pytorch Module into tagger dict
        name = getattr(model_name_or_path, 'name', model_name_or_path)
        if not self.token_taggers[name]:
            """
            self.token_taggers[model_name_or_path] = SequenceTagger.load(
                model_name_or_path
            )
            """
            if risinstance([FlairModelResult, HFModelResult], model_name_or_path):
                try:
                    self.token_taggers[name] = FlairTokenTagger.load(name)
                except:
                    self.token_taggers[name] = TransformersTokenTagger.load(name)
            elif risinstance([str, Path], model_name_or_path) and (Path(model_name_or_path).exists() and Path(model_name_or_path).is_dir()):
                # Load in previously existing model
                try:
                    self.token_taggers[name] = FlairTokenTagger.load(name)
                except:
                    self.token_taggers[name] = TransformersTokenTagger.load(name)
            else:
                _flair_hub = FlairModelHub()
                _hf_hub = HFModelHub()
                res = _flair_hub.search_model_by_name(name, user_uploaded=True)
                if len(res) < 1:
                    # No models found
                    res = _hf_hub.search_model_by_name(name, user_uploaded=True)
                    if len(res) < 1:
                        logger.info("Not a valid `model_name_or_path` param")
                        return [Sentence('')]
                    else:
                        res[0].name.replace('flairNLP', 'flair')
                        self.token_taggers[res[0].name] = TransformersTokenTagger.load(res[0].name)
                        name = res[0].name

                else:
                    name = res[0].name.replace('flairNLP/', '')
                    self.token_taggers[name] = FlairTokenTagger.load(name) # Returning the first should always be the non-fast option

        tagger = self.token_taggers[name]
        return tagger.predict(
            text=text,
            mini_batch_size=mini_batch_size,
            **kwargs,
        )

    def tag_all(
        self,
        text: Union[List[Sentence], Sentence, List[str], str], # Text input, it can be a string or any of Flair's `Sentence` input formats
        mini_batch_size: int = 32, # The mini batch size for running inference
        **kwargs, # Keyword arguments for Flair's `SequenceTagger.predict()` method
    ) -> List[Sentence]:
        """Tags tokens with all labels from all token classification models

        **Returns**: A list of Flair's `Sentence`'s
        """
        if len(self.token_taggers) == 0:
            print("No token classification models loaded...")
            return Sentence()
        sentences = text
        for tagger_name in self.token_taggers.keys():
            sentences = self.tag_text(
                sentences,
                model_name_or_path=tagger_name,
                mini_batch_size=mini_batch_size,
                **kwargs,
            )
        return sentences