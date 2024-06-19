FROM python:3.11-slim
ENV ROOT_DIR=/tests
WORKDIR $ROOT_DIR

COPY build/wallet_api_backend_tests/requirements.txt $ROOT_DIR/requirements.txt
RUN pip install -r $ROOT_DIR/requirements.txt
