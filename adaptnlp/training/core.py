# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/14_training.core.ipynb (unless otherwise specified).

__all__ = ['ParentLabeller', 'ColReader', 'Categorize', 'RandomSplitter', 'TaskDatasets', 'AdaptiveTuner']

# Cell
from fastcore.xtras import Path, range_of # pathlib `Path` with extra bits
from fastcore.foundation import mask2idxs, L
from fastcore.meta import delegates

from fastai.learner import *
from fastai.data.all import *
from fastai.callback.all import *
from fastai.metrics import *
from fastai.losses import *
from fastai.optimizer import *
## Note: Eventually get more specific about this

from fastai.data.core import DataLoaders

from torch.utils.data import DataLoader

from transformers import default_data_collator, AutoTokenizer
import torch

# Cell
class ParentLabeller:
    """
    Extracts class based on filename's parent at `level`
    """
    def __init__(
        self,
        level=1 # The level up from `fname` to find the label
    ):
        self.level = level

    def __call__(self, o:Path): return self._do_level(o, self.level)

    def _do_level(self, o:Path, level:int):
        "Goes down one level on parent"
        def _inner(a): return a.parent
        if level == 1: return o.parent.name
        else: return self._do_level(_inner(o), level - 1)

# Cell
class ColReader:
    """
    Reads `cols` in `row` with potential `pref` and `suff`
    Based on the fastai class
    """
    def __init__(
        self,
        cols, # Some column names to use
        pref:str='', # A prefix
        suff:str='', # A suffix
        label_delim:str=None, # A label delimiter
    ):
        self.pref = str(pref) + os.path.sep if isinstance(pref, Path) else pref
        self.suff, self.label_delim = suff, label_delim
        self.cols = L(cols)

    def _do_one(self, r, c):
        o = r[c] if isinstance(c,int) else r[c] if c=='name' or c=='cat' else getattr(r,c)
        if len(self.pref)==0 and len(self.suff)==0 and self.label_delim is None: return o
        if self.label_delim is None: return f'{self.pref}{o}{self.suff}'
        else: return o.split(self.label_delim) if len(o)>0 else []

    def __call__(self, o):
        if len(self.cols) == 1: return self._do_one(o, self.cols[0])
        return L(self._do_one(o,c) for c in self.cols)

# Cell
class Categorize:
    """
    Collection of categories with reverse mapping in `o2i`
    Based on the fastai class
    """
    def __init__(
        self,
        names, # An interable collection of items to create a vocab from
        sort=True # Whether to make the items sorted
    ):
        names = L(names)
        self.classes = L(o for o in names.unique() if o == o)
        if sort: self.classes = self.classes.sorted()
        self.o2i = dict(self.classes.val2idx())

    def map_objs(
        self,
        objs # Some iterable collection
    ):
        "Map `objs` to IDs"
        return L(self.o2i[o] for o in objs)

    def map_ids(
        self,
        ids # Some ids correlating to `self.classes`
    ):
        "Map `ids` to objects in vocab"
        return L(self.classes[o] for o in ids)

    def __call__(self, o):
        "Label encode a single `o`"
        return int(self.o2i[o])

    def decode(self, o): return self.classes[o]

# Cell
def RandomSplitter(valid_pct=0.2, seed=None):
    """
    Creates a function that splits some items between train and validation with `valid_pct` randomly
    Based on the fastai class
    """
    def _inner(o):
        if seed is not None: torch.manual_seed(seed)
        rand_idx = L(list(torch.randperm(len(o)).numpy()))
        cut = int(valid_pct * len(o))
        return rand_idx[cut:], rand_idx[:cut]
    return _inner

# Cell
class TaskDatasets:
    """
    A set of datasets for a particular task, with a simple API.

    Note: This is the base API, `items` should be a set of regular text and model-ready labels,
          including label or one-hot encoding being applied.
    """
    def __init__(
        self,
        train_dset, # A train `Dataset` object
        valid_dset, # A validation `Dataset` object
        tokenizer_name:str = None, # The string name of a `HuggingFace` tokenizer or model. If `None`, will not tokenize the dataset.
        tokenize:bool = True, # Whether to tokenize the dataset immediatly
        tokenize_kwargs:dict = {}, # Some kwargs for when we call the tokenizer
        auto_kwargs:dict = {}, # Some kwargs when calling `AutoTokenizer.from_pretrained`
    ):
        self.train = train_dset
        self.valid = valid_dset
        self.tokenizer = None
        if tokenizer_name is not None: self.set_tokenizer(tokenizer_name, **auto_kwargs)
        if self.tokenizer:
            if 'max_length' in tokenize_kwargs.keys() and self.tokenizer.model_max_length >= tokenize_kwargs['max_length']: pass
            elif 'max_length' in tokenize_kwargs.keys() and self.tokenizer.model_max_length < tokenize_kwargs['max_length']:
                print("Warning: `max_length` is larger than the pretrained model")
            elif 'max_length' not in tokenize_kwargs.keys():
                print("No value for `max_length` set, automatically adjusting to the size of the model and including truncation")
                tokenize_kwargs['max_length'] = self.tokenizer.model_max_length
                tokenize_kwargs['truncation'] = True
                print(f"Sequence length set to: {tokenize_kwargs['max_length']}")
        if tokenize and self.tokenizer is not None: self._tokenize(**tokenize_kwargs)
        elif tokenize and self.tokenizer is None:
            print("Tried to tokenize a dataset without a tokenizer. Please set a tokenizer with `set_tokenizer` and call `_tokenize()`")


    def __getitem__(self, idx): return self.train[idx]

    def _tokenize(self, **kwargs):
        "Tokenize dataset in `self.items` with `kwargs` for `tokenize()`"
        if not self.tokenizer: raise ValueError("Tried to tokenize a dataset without a tokenizer. Please add a tokenizer with `set_tokenizer(tokenizer_name` and try again")
        def _inner(item):return self.tokenizer(item['text'], **kwargs)
        self.train = self.train.map(_inner,batched=True,remove_columns = ['text'])
        self.valid = self.valid.map(_inner,batched=True,remove_columns = ['text'])

    @delegates(AutoTokenizer.from_pretrained)
    def set_tokenizer(
        self,
        tokenizer_name:str, # A string name of a `HuggingFace` tokenizer or model
        override_existing:bool = False, # Whether to override an existing tokenizer
        **kwargs # kwargs to go to `AutoTokenizer.from_pretrained`
    ):
        "Sets a new `AutoTokenizer` to `self.tokenizer`"
        if self.tokenizer and not override_existing:
            print(f'Warning! You are trying to override an existing tokenizer: {self.tokenizer.name_or_path}. Pass `override_existing=True` to use a new tokenizer')
            return
        elif self.tokenizer and override_existing:
            print(f'Setting new tokenizer to {tokenizer_name}')
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name, **kwargs)
        except:
            raise ValueError(f'{tokenizer_name} is not a valid pretrained model on the HuggingFace Hub or a local model')

    @delegates(DataLoaders)
    def dataloaders(
        self,
        batch_size=8, # A batch size
        shuffle_train=True, # Whether to shuffle the training dataset
        collate_fn = None, # A custom collation function
        **kwargs): # Torch DataLoader kwargs
        "Creates `DataLoaders` from the dataset"
        if collate_fn is None: collate_fn = default_data_collator
        train_dl = DataLoader(self.train, shuffle=shuffle_train, collate_fn=collate_fn, batch_size=batch_size, **kwargs)
        valid_dl = DataLoader(self.valid, shuffle=False, collate_fn=collate_fn, batch_size=batch_size, **kwargs)
        return DataLoaders(train_dl, valid_dl)

# Cell
class _AdaptiveLearner(Learner):
    """
    A base fastai `Learner` that overrides `_split` and `_do_one_batch` to
    have it work with HuggingFace datasets and models
    """
    def _split(self, b):
        "Assign `self.xb` to model input and labels"
        self.xb = b
        if 'labels' in b.keys(): self.yb = b['labels'].unsqueeze(0)

    def _do_one_batch(self):
        "Move a batch of data to a device, get predictions, calculate the loss, and perform backward pass"
        self.xb = {k:v.to(self.device) for k,v in self.xb.items()} # See if `to_device` fixes this
        self.yb = self.yb.to(self.device)
        out = self.model(**self.xb)
        self.pred = out['logits'].to(self.device)
        self('after_pred')
        self.loss_grad = out['loss'].to(self.device)
        self.loss = self.loss_grad.clone()
        self('after_loss')
        if not self.training or not len(self.yb): return
        self('before_backward')
        self.loss_grad.backward()
        self._with_events(self.opt.step, 'step', CancelStepException)
        self.opt.zero_grad()

# Cell
mk_class('Strategy', **{'OneCycle':'fit_one_cycle', 'CosineAnnealing':'fit_flat_cos', 'SGDR':'fit_sgdr'}, doc_string='Class for fitting strategies with typo-proofing')

# Cell
class AdaptiveTuner:
    """
    A base `Tuner` that interfaces with `AdaptiveLearner` with specific exposed functions
    """
    @delegates(_AdaptiveLearner.__init__)
    def __init__(self, expose_fastai:bool=False, **kwargs):
        self._tuner = _AdaptiveLearner(**kwargs)

        exposed_attrs = ['dls', 'model', 'loss_func', 'metrics']
        for attr in exposed_attrs:
            setattr(self, attr, getattr(self._tuner, attr))
        if expose_fastai:
            cls = self.__class__
            self.__class__ = cls.__class__("AdaptiveTuner", (cls, _AdaptiveLearner), kwargs)

    def tune(
        self,
        epochs:int, # Number of epochs to train for
        lr:float = None, # If None, finds a new LR and uses suggestion_method
        strategy:Strategy = Strategy.OneCycle,
        callbacks = [], # Extra fastai Callbacks
        **kwargs ## kwargs for the fit function

    ):
        "Fine tune `self.model` for `epochs` with an `lr` and `strategy`"
        func = getattr(self, strategy, getattr(self._tuner, strategy, None))
        for attr in 'epochs,lr,cbs'.split():
            if attr in kwargs.keys(): kwargs.pop(attr)
        func(epochs, lr, cbs=callbacks, **kwargs)

    @delegates(Learner.lr_find)
    def lr_find(self, **kwargs): return self._tuner.lr_find(**kwargs)

    def save(self, file:Union[Path,str], with_opt=True, pickle_protocol=2):
        file = join_path_file(kwargs['file'], self.path/self.model_dir, ext='.pth')
        if rank_distrib(): return # Don't save if child proc
        opt = getattr(self, 'opt', None)
        if opt is None: with_opt = False
        state = get_model(self.model).state_dict()
        state = {'model':state}
        if with_opt: state['opt'] = opt.state_dict()
        state['model_name_or_path'] = self.model.name_or_path
        torch.save(state, file, pickle_protocol=pickle_protocol)
        return file

    def load(self, file:Union[Path,str], device=None, with_opt=True, strict=True):
        if device is None and hasattr(self.dls, 'device'): device = self.dls.device
        if self.opt is None: self.create_opt()
        file = join_path_file(file, self.path/self.model_dir, ext='.pth')
        distrib_barrier()
        if isinstance(device, int): device = torch.device('cuda', device)
        elif device is None: device='cpu'
        state = torch.load(file, map_location=device)
        hasopt = 'opt' in state.keys()
        model_state = state['model']
        get_model(self.model).load_state_dict(model_state, strict=strict)
        if hasopt and with_opt:
            try: self.opt.load_state_dict(state['opt'])
            except:
                if with_opt: warn("Could not load the optimizer state.")
        elif with_opt: warn("Saved file doesn't contain an optimizer state")
        return self

for attr in ['lr_find', 'save', 'load']:
    setattr(getattr(AdaptiveTuner, attr), '__doc__', getattr(_AdaptiveLearner, attr).__doc__)