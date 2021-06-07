FROM novetta/adaptnlp:latest

# For SSL/TLS for requests
ENV REQUESTS_CA_BUNDLE /etc/ssl/certs/ca-certificates.crt
ENV SERVER_PORT 5000
ENV SERVER_HOST 0.0.0.0

# Statements and log messages
ENV PYTHONUNBUFFERED True

# Default ARG vars for model configuration
ARG SEQUENCE_CLASSIFICATION_MODEL=nlptown/bert-base-multilingual-uncased-sentiment

ENV SEQUENCE_CLASSIFICATION_MODEL ${SEQUENCE_CLASSIFICATION_MODEL}

# Expose typical endpoints
EXPOSE 8888
EXPOSE 5000

WORKDIR /adaptnlp-rest

COPY . /adaptnlp-rest

RUN pip3 install -r requirements.txt

RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
