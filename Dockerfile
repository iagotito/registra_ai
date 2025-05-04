FROM python:3.13-alpine as base

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="${VIRTUAL_ENV}/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="${PYTHONPATH}:/app"

RUN apk update && apk upgrade && \
    apk add --no-cache --virtual build-dependencies \
        make \
        g++

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN python3 -m venv $VIRTUAL_ENV

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app/app
COPY ./alembic /app/alembic
COPY ./alembic.ini /app/alembic.ini

RUN apk del build-dependencies

EXPOSE 8000

CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
