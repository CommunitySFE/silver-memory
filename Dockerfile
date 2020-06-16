FROM python:alpine

WORKDIR /opt/sfe-utilities

COPY requirements.txt .

RUN apk update && apk add gcc musl-dev && pip install -r requirements.txt

COPY . .

ENTRYPOINT [ "python", "main.py" ]