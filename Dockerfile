FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

RUN pip install requests
RUN pip install pymemcache

COPY ./app /app
COPY ./static /app/static/
