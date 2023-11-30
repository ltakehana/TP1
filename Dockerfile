FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

WORKDIR /usr/src/app

COPY . /usr/src/app

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
