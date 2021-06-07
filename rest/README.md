# AdaptNLP-Rest API

## Quick Start

### Docker Hub
The docker image of AdaptNLP is built with the `novetta/adaptnlp:latest` image.

The docker image of AdaptNLP's NLP task rest services are hosted on Docker Hub as well, identified by `adaptnlp:{VERSION_NUMBER}-api-{TASK}` naming convention

Every image can be pulled and run by running the following:

- Token Tagging
  - `docker run -itp 5000:5000 -e TOKEN_TAGGING_MODE=ner -e TOKEN_TAGGING_MODE=ner-ontonotes-fast novetta/adaptnlp:latest-api-token-tagging bash`
- Sequence Classification
  - `docker run -itp 5000:5000 -e SEQUENCE_CLASSIFICATION_MODEL=nlptown/bert-base-multilingual-uncased-sentiment novetta/adaptnlp:latest-api-sequence-classification bash`
- Question Answering
  - `docker run -itp 5000:5000 -e QUESTION_ANSWERING_MODEL=distilbert-base-uncased-distilled-squad novetta/adaptnlp:latest-api-question-answering bash`
- Translation 
  - `docker run -itp 5000:5000 -e TRANSLATION_MODEL=Helsinki-NLP/opus-mt-ar-e novetta/adaptnlp:translation-api-latest bash`
- Summarization 
  - `docker run -itp 5000:5000 -e SUMMARIZATION_MODEL=facebook/bart-large-cnn novetta/adaptnlp:summarization-api-latest bash`
- Text Generation 
  - `docker run -itp 5000:5000 -e TEXT_GENERATION_MODEL=gpt2 novetta/adaptnlp:text-generation-api-latest bash`

Note: Add the `--gpus` arg parameter if you'd like the images and endpoints to run with GPUs. You need to have NVIDIA Docker installed with a CUDA-compatible GPU.

## Build and Run
Manually build and run your own docker images and deploy endpoints by following one of the below methods:

### 1. Docker Build Env Arg Entries
Specify the pretrained models you want to use for the endpoints.  These can be Transformers pre-trained models, Flair's pre-trained models,
or your own custom trained models with a path pointing to the model.  (The model must be in the directory you are building your image from for your
respective NLP task)

**Token Tagger**
```
docker build -t token-tagging:latest --build-arg TOKEN_TAGGING_MODE=ner \
                                     --build-arg TOKEN_TAGGING_MODEL=ner-ontonotes-fast .
docker run -itp 5000:5000 token-tagging:latest bash
```
To run with GPUs if you have nvidia-docker installed with with compatible NVIDIA drivers
```
docker run -itp 5000:5000 --gpus all token-tagging:latest bash
```

**Sequence Classifier**
```
docker build -t sequence-classification:latest --build-arg SEQUENCE_CLASSIFICATION_MODEL=nlptown/bert-base-multilingual-uncased-sentiment .
docker run -itp 5000:5000 sequence-classification:latest bash
```
To run with GPUs if you have nvidia-docker installed with with compatible NVIDIA drivers
```
docker run -itp 5000:5000 --gpus all sequence-classification:latest bash
```

**Question Answering**
```
docker build -t question-answering:latest --build-arg QUESTION_ANSWERING_MODEL=distilbert-base-uncased-distilled-squad .
docker run -itp 5000:5000 question-answering:latest bash
```
To run with GPUs if you have nvidia-docker installed with with compatible NVIDIA drivers
```
docker run -itp 5000:5000 --gpus all question-answering:latest bash
```

**Translation**
```
docker build -t translation:latest --build-arg TRANSLATION_MODEL=Helsinki-NLP/opus-mt-ar-e .
docker run -itp 5000:5000 translation:latest bash
```
To run with GPUs if you have nvidia-docker installed with with compatible NVIDIA drivers
```
docker run -itp 5000:5000 --gpus all translation:latest bash
```

**Summarization**
```
docker build -t summarization:latest --build-arg SUMMARIZATION_MODEL=facebook/bart-large-cnn .
docker run -itp 5000:5000 summarization:latest bash
```
To run with GPUs if you have nvidia-docker installed with with compatible NVIDIA drivers
```
docker run -itp 5000:5000 --gpus all summarization:latest bash
```

**Text Generation**
```
docker build -t text-generation:latest --build-arg TEXT_GENERATION_MODEL=gpt2 .
docker run -itp 5000:5000 text-generation:latest bash
```
To run with GPUs if you have nvidia-docker installed with with compatible NVIDIA drivers
```
docker run -itp 5000:5000 --gpus all text-generation:latest bash
```


### 2. Docker Run Env Arg Entries
Sometimes you may wont to specify the models as environment variables in docker post-build for convience or other reasons. To do so use the below commands to deploy any of the above NLP task services. The example below runs the token classification service.
```
docker build -t token-tagging:latest .
docker run -itp 5000:5000 -e TOKEN_TAGGING_MODE='ner' \
                          -e TOKEN_TAGGING_MODEL='ner-ontonotes-fast' \
                          token-tagging:latest \
                          bash
```
To run with GPUs if you have nvidia-docker installed with with compatible NVIDIA drivers
```
docker run -itp 5000:5000 --gpus all -e TOKEN_TAGGING_MODE='ner' \
                                     -e TOKEN_TAGGING_MODEL='ner-ontonotes-fast' \
                                     token-tagging:latest \
                                     bash
```                                                           

### 3. Local
If you just want to run the rest services locally in an environment that has AdaptNLP installed, you can 
run the following in whichever NLP task directory you would like.

```
pip install -r requirements
export TOKEN_TAGGING_MODE=ner
export TOKEN_TAGGING_MODEL=ner-ontonotes-fast
export SEQUENCE_CLASSIFICATION_MODEL=en-sentiment
export QUESTION_ANSWERING_MODEL=distilbert-base-uncased-distilled-squad
uvicorn app.main:app --host 0.0.0.0 --port 5000

```

## SwaggerUI

Access SwaggerUI console by going to `localhost:5000/docs` after deploying

![Swagger Example](https://raw.githubusercontent.com/novetta/adaptnlp/master/docs/img/fastapi-docs.png)

