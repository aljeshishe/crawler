# syntax = docker/dockerfile:experimental
FROM public.ecr.aws/lambda/python:3.8


ENV YOUR_ENV=production \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  # PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.2.2

WORKDIR ${LAMBDA_TASK_ROOT}

COPY requirements.txt ./
RUN --mount=type=cache,mode=0777,target=/root/.cache pip install -r requirements.txt

COPY .env *.py .serverless-wsgi Procfile ./
COPY assets ./assets
CMD [ "wsgi_handler.handler" ]
