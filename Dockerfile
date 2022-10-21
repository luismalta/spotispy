FROM python:3.10-slim

WORKDIR /opt/dagster/app

COPY . /opt/dagster/app

RUN pip install .

WORKDIR /opt/dagster/app/spotispy

EXPOSE 4000

CMD ["dagster", "api", "grpc", "-h", "0.0.0.0", "-p", "4000", "-f", "repository.py"]