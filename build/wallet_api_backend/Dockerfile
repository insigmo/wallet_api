FROM python:3.11-slim
ENV ROOT_DIR=/app
WORKDIR $ROOT_DIR

RUN apt-get update && apt-get install -y default-libmysqlclient-dev

COPY requirements.txt $ROOT_DIR/requirements.txt
RUN pip install -r $ROOT_DIR/requirements.txt
COPY build/wallet_api_backend/supervisord/*conf /etc/supervisor/supervisor.d/
COPY build/wallet_api_backend/entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
