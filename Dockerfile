FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

RUN pip install requests
RUN pip install pymemcache pytest

COPY ./app /app
COPY ./static /app/static/
