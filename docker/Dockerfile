# Based on https://github.com/fastai/docker-containers/blob/master/fastai-build/Dockerfile

# Install cuda-compatible torch
FROM pytorch/pytorch:1.8.1-cuda11.1-cudnn8-runtime

ARG BUILD=dev

# Install git and Jupyter
RUN apt-get update && apt-get install -y git
RUN pip install jupyter

# Clone adaptnlp
RUN git clone https://github.com/novetta/adaptnlp.git --depth 1

# Build environment based on type
RUN /bin/bash -c "if [[ $BUILD == 'prod' ]] ; then echo \"Production Build\" && cd adaptnlp && pip install .; fi"
RUN /bin/bash -c "if [[ $BUILD == 'dev' ]] ; then echo \"Development Build\" && cd adaptnlp && pip install -e \".[dev]\" ; fi"

# Start server
RUN jupyter notebook --ip=0.0.0 --no-browser --allow-root --port=8888 --NotebookApp.token="" --NotebookApp.password="" --NotebookApp.allow_origin="*"
