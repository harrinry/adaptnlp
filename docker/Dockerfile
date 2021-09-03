# Based on https://github.com/fastai/docker-containers/blob/master/fastai-build/Dockerfile

FROM nvcr.io/nvidia/cuda:10.2-runtime-ubuntu18.04

ARG BUILD=dev

# Set python env vars
ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# Install python
# Add deadsnakes ppa for python version >= 3.8.2
RUN apt-get update && \
    apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get install -y --no-install-recommends \
    build-essential \
    python3.8 \
    python3.8-dev \
    python3.8-venv\
    python3-pip \
    curl \
    git
    
# Setup venv
ENV VIRTUAL_ENV=/opt/venv
RUN python3.8 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip install pip -U

# Install git and Jupyter
RUN pip install jupyter

# Clone adaptnlp
RUN git clone https://github.com/novetta/adaptnlp.git --depth 1

# Build environment based on type
RUN /bin/bash -c "if [[ $BUILD == 'prod' ]] ; then echo \"Production Build\" && cd adaptnlp && pip install .; fi"
RUN /bin/bash -c "if [[ $BUILD == 'dev' ]] ; then echo \"Development Build\" && cd adaptnlp && pip install -e \".[dev]\" ; fi"

RUN pip install jupyterlab==3.0.16 jupyter_server==1.6.4 xeus-python

# Start server
CMD ["sh","-c", "jupyter notebook --ip=0.0.0.0 --no-browser --allow-root --port=8888 --NotebookApp.token='' --NotebookApp.password='' --NotebookApp.allow_origin='*' --NotebookApp.base_url=${NB_PREFIX}"]
