# Based on https://github.com/fastai/docker-containers/blob/master/fastai-build/Dockerfile

FROM nvcr.io/nvidia/cuda:10.2-runtime-ubuntu18.04

ARG BUILD=dev

# Install git and Jupyter
RUN apt-get update && apt-get install -y git
RUN pip install jupyter

# Clone adaptnlp
RUN git clone https://github.com/novetta/adaptnlp.git --depth 1

# Build environment based on type
RUN /bin/bash -c "echo \"Production Build\" && cd adaptnlp && pip install .;"
RUN /bin/bash -c "if [[ $BUILD == 'dev' ]] ; then echo \"Development Build\" && cd adaptnlp && pip install -e \".[dev]\" ; fi"

# Start server
CMD ["sh","-c", "jupyter notebook --ip=0.0.0.0 --no-browser --allow-root --port=8888 --NotebookApp.token='' --NotebookApp.password='' --NotebookApp.allow_origin='*' --NotebookApp.base_url=${NB_PREFIX}"]
