FROM python:3.10-slim


ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.0.0

# System deps:
RUN pip install poetry


# Setup project source code
RUN mkdir -p /opt/dagster/app
ENV DAGSTER_HOME=/opt/dagster/app
WORKDIR /opt/dagster/app
COPY . .


# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

EXPOSE 3000

CMD ["dagit", "-h", "0.0.0.0", "-p", "3000"]
