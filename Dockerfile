FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

RUN pip install requests
RUN pip install pymemcache pytest
RUN pip install --upgrade pip && \
    pip install poetry

COPY ./app /app
COPY ./static /app/static/
COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false && \
    poetry install --no-dev