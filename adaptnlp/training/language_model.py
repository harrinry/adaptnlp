# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/16_training.language_model.ipynb (unless otherwise specified).

__all__ = ['LanguageModelDatasets']

# Cell
from transformers import DataCollatorForLanguageModeling, default_data_collator

from .core import *

from fastai.data.core import DataLoaders

import pandas as pd
from fastcore.meta import delegates

# Internal Cell
def _group_texts(examples, block_size):
    # Concatenate all texts, based on code by Transformers
    concatenated_examples = {k: sum(examples[k], []) for k in examples.keys()}
    total_length = len(concatenated_examples[list(examples.keys())[0]])
    # We drop the small remainder, we could add padding if the model supported it instead of this drop, you can
    # customize this part to your needs.
    total_length = (total_length // block_size) * block_size
    # Split by chunks of max_len.
    result = {
        k: [t[i : i + block_size] for i in range(0, total_length, block_size)]
        for k, t in concatenated_examples.items()
    }
    result["labels"] = result["input_ids"].copy()
    return result

# Cell
class LanguageModelDatasets(TaskDatasets):
    """
    A set of datasets designed for language model fine-tuning
    """
    def __init__(
        self,
        items, # Some items we can pull x's and y's from
        get_x = ColReader('text'), # A function taking in one item and extracting the text
        block_size:int = 512, # A block size to split up the data with. Note: this is different than `max_len`
        masked_lm:bool=False, # Whether this is a Masked Language Model
        splits = None, # Indexs to split the data from
        tokenizer_name:str = None, # The string name of a `HuggingFace` tokenizer or model. If `None`, will not tokenize the dataset.
        tokenize:bool = True, # Whether to tokenize the dataset immediatly
        tokenize_kwargs:dict = {}, # Some kwargs for when we call the tokenizer
        auto_kwargs:dict = {}, # Some kwargs when calling `AutoTokenizer.from_pretrained`
    ):
        xs = L(L(items).map(get_x)[0].values, use_list=True)
        train_xs = xs[splits[0]]
        valid_xs = xs[splits[1]]

        train_dset = Dataset.from_dict({
            'text':train_xs.items
        })

        valid_dset = Dataset.from_dict({
            'text':valid_xs.items
        })

        super().__init__(train_dset, valid_dset, tokenizer_name, tokenize, tokenize_kwargs, auto_kwargs)
        self.masked_lm = masked_lm
        self.block_size = block_size
        f = partial(_group_texts, block_size=self.block_size)
        self.train = self.train.map(f, batched=True)
        self.valid = self.valid.map(f, batched=True)

    @classmethod
    def from_df(
        cls,
        df:pd.DataFrame, # A Pandas Dataframe or Path to a DataFrame
        text_col:str = 'text', # Name of the column the text is stored
        splits = None, # Indexes to split the data with
        block_size:int = 512, # A block size to split up the data with. Note: this is different than `max_len`
        masked_lm:bool=False, # Whether this is a Masked Language Model
        tokenizer_name:str = None, # The string name of a `HuggingFace` tokenizer or model. If `None`, will not tokenize the dataset.
        tokenize:bool = True, # Whether to tokenize the dataset immediatly
        tokenize_kwargs:dict = {}, # Some kwargs for when we call the tokenizer
        auto_kwargs:dict = {}, # Some kwargs when calling `AutoTokenizer.from_pretrained`
    ):
        "Builds `SequenceClassificationDatasets` from a `DataFrame` or file path"
        get_x = ColReader(text_col)
        if splits is None: splits = RandomSplitter(0.2)(range_of(df))
        return cls(df, get_x, block_size, masked_lm, splits, tokenizer_name, tokenize, tokenize_kwargs, auto_kwargs)

    @delegates(DataLoaders)
    def dataloaders(
        self,
        batch_size=8, # A batch size
        shuffle_train=True, # Whether to shuffle the training dataset
        collate_fn = default_data_collator, # A custom collation function
        mlm_probability:float = 0.15, # Token masking probablity for Masked Language Models
        **kwargs): # Torch DataLoader kwargs
        if self.masked_lm: collate_fn = DataCollatorForLanguageModeling(tokenizer=self.tokenizer, mlm_probability=mlm_probability)
        return super().dataloaders(batch_size, shuffle_train, collate_fn, **kwargs)