FROM python:3.9-slim

RUN pip install 'poetry==1.1.6'
COPY ./pyproject.toml /tmp/
COPY ./poetry.lock /tmp/
RUN cd /tmp && poetry export -f requirements.txt > requirements.txt
RUN pip install -r /tmp/requirements.txt

WORKDIR  /app
COPY app /app/app
RUN mkdir static

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
