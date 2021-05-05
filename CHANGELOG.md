# Release Notes

## 0.2.3

### Breaking Changes:
- New versions of AdaptNLP will require a minimum torch version of 1.7, and flair of 0.9 (currently we install via git until 0.9/0.81 is released)

### New Features

- Complete conversion to the [nbdev](nbdev.fast.ai) library format and actions

- Complete revamp of the [documentation](novetta.github.io/adaptnlp)

- Inference API entirely relies on [fastai_minima](https://github.com/muellerzr/fastai_minima) and is now built on [fastai](https://github.com/fastai/fastai)'s [Callback System](https://docs.fast.ai/callback.core#Callback)

- Integration with [fastcore](fastcore.fast.ai) to simplify logic

- [HuggingFace](https://novetta.github.io/adaptnlp/model_hub.html#HFModelHub) and [Flair](https://novetta.github.io/adaptnlp/model_hub.html#FlairModelHub) [ModelHubs](https://novetta.github.io/adaptnlp/model_hub.html), an easier API to interact, search, and download HF and Flair models. Uses [huggingface_hub](https://github.com/huggingface/huggingface_hub) as a backend. Has logged every single Flair model, including those not in the HuggingFace API

### Bugs Squashed

- Fix accessing bart-large-cnn ([110](https://github.com/Novetta/adaptnlp/issues/110))
- Fix SAVE_STATE_WARNING ([114](https://github.com/Novetta/adaptnlp/issues/114))

## 0.2.2

### Official AdaptNLP Docker Images updated
- Using NVIDIA NGC Container Registry Cuda base images #101 
- All images should be deployable via. Kubeflow Jupyter Servers
- Cleaner python virtualvenv setup #101 
- Official readme can be found at https://github.com/Novetta/adaptnlp/blob/master/docker/README.md

### Minor Bug Fixes
- Fix token tagging REST application type check #92 
- Semantic fixes in readme #94 
- Standalone microservice REST application images #93 
- Python 3.7+ is now an official requirement #97

## 0.2.1

Updated to nlp 0.4 -> datasets 1.0+ and multi-label training for sequence classification fixes.

### `EasySequenceClassifier.train()` Updates
- Integrates `datasets.Dataset` now
- Swapped order of formatting and label column renaming due to labels not showing up from torch data batches #87 

### Tutorials and Documentation
- Documentation and sequence classification tutorials have been updated to address nlp->datasets name change
- Broken links also updated


### ODSC Europe Workshop 2020: Notebooks and Colab
- ODSC Europe 2020 workshop materials now available in repository "/tutorials/Workshop"
- Easy to run notebooks and colab links aligned with the tutorials are available



## 0.2.0

Updated to transformers 3+, nlp 0.4+, flair 0.6+, pandas 1+

New Features!

### New and "easier" training framework with easy modules: `EasySequenceClassifier.train()` and `EasySequenceClassifier.evaluate()`
- Integrates `nlp.Dataset` and `transformers.Trainer` for a streamlined training workflow
- Tutorials, notebooks, and colab links available
- Sequence Classification task has been implemented, other NLP tasks are in the works
- `SequenceClassifierTrainer` is still available, but will be transitioned into the `EasySequenceClassifier` and deprecated

### New and "easier" `LMFineTuner` 
- Integrates `transformers.Trainer` for a streamlined training workflow
- Older `LMFineTuner` is still available as `LMFineTunerManual`, but will be deprecated in later releases
- Tutorials, notebooks, and colab links available

### `EasyTextGenerator`
- New module for text generation. GPT models are currently supported, other models may work but still experimental
- Tutorials, notebooks, and colab links available

### Tutorials and Documentation
- Documentation has been edited and updated to include additional features like the change in training frameworks and fine-tuning
- The sequence classification tutorial is a good indicator of the direction we are going with the training and fine-tuning framework


### Notebooks and Colab
- Easy to run notebooks and colab links aligned with the tutorials are available

### Bug fixes
- Minor bug and implementation error fixes from flair upgrades


## 0.1.6
Split dev requirements #29 #66 
Pinned torch #70 

## 0.1.5
Updated to Transformers 2.8.0 which now includes the ELECTRA language model

### `EasySummarizer` and `EasyTranslator` Bug Fix #63 
- Address mini batch output format issue for language model heads for the summarization and translation task

### Tutorials and Workshop #64 
- Add the ODSC Timeline Generator notebooks along with colab links
- Small touch ups in tutorial notebooks

### Documentation
- Address missing `model_name_or_path` param in some easy modules

## 0.1.4
Updated to Transformers 2.7.0 which includes the Bart and T5 Language Models!

### `EasySummarizer` #47 
- New module for summarizing documents.  These support both the T5 and Bart pre-trained models provided by Hugging Face.
- Helper objects for the easy module that can be run as standalone instances
`TransformersSummarizer`

### `EasyTranslator` #49
- New module for translating documents with T5 pre-trained models provided by Hugging Face.
- Helper objects for the easy module that can be run as standalone instances
`TransformersTranslator`

### Documentation and Tutorials #52
- New Class API documentation for `EasySummarizer` and `EasyTranslator`
- New tutorial guides, initial notebooks, and links to colab for the above as well
- Readme provides quickstart samples that show examples from the notebooks #53 

### Other
- Dockerhub repo for adaptnlp-rest added here https://hub.docker.com/r/achangnovetta/adaptnlp-rest 
- Upgraded CircleCI allowing us to run #40 
- Added Nightly build #39 


## 0.1.3
Sequence Classification and Question Answering updates to integrate Hugging Face's public models.

### `EasySequenceClassifier`
- Can now take Flair and Transformers pre-trained sequence classification models as input in the `model_name_or_path` param
- Helper objects for the easy module that can be run as standalone instances
`TransformersSequenceClassifier`
`FlairSequenceClassifier`

### `EasyQuestionAnswering`
- Can now take Transformers pre-trained sequence classification models as input in the `model_name_or_path` param
- Helper objects for the easy module that can be run as standalone instances
`TransformersQuestionAnswering`

### Documentation and Tutorials
Documentation has been updated with the above implementations
- Tutorials updated with better examples to convey changes
- Class API docs updated
- Tutorial notebooks updated
- Colab notebooks better displayed on readme

### FastAPI Rest
FastAPI updated to latest (0.52.0)
FastAPI endpoints can now be stood up and deployed with any huggingface sequence classification or question answering model specified as an env var arg.


### Dependencies
Transformers pinned for stable updates


## 0.1.2 - Initial Release of AdaptNLP

AdaptNLP's first published release on github.

### Easy API:
  - `EasyTokenTagger`
  - `EasySequenceClassifier`
  - `EasyWordEmbeddings`
  - `EasyStackedEmbeddings`
  - `EasyDocumentEmbeddings`

### Training and Fine-tuning Interface
  - `SequenceClassifierTrainer`
  - `LMFineTuner`

### FastAPI AdaptNLP App for Streamlined Rapid NLP-Model Deployment
  - adaptnlp/rest
  - configured to run any pretrained and custom trained flair/adaptnlp models
  - compatible with nvidia-docker for GPU use
  - AdaptNLP integration but loosely coupled

### Documentation
  - Documentation release with walk-through guides, tutorials, and Class API docs of the above
  - Built with mkdocs, material for mkdocs, and mkautodoc

### Tutorials
  - IPython/Colab Notebooks provided and updated to showcase AdaptNLP Modules

### Continuous Integration
  - CircleCI build and tests running successfully and minimally
  - Github workflow for pypi publishing added

### Formatting
  - Flake8 and Black adherence
