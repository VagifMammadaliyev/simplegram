FROM python:3.9-alpine

ENV PYTHONUNBUFFERED 1

RUN apk update && apk add build-base libffi-dev

COPY ./requirements /requirements
RUN pip install -r /requirements/base.txt

WORKDIR /code

COPY ./src /code

EXPOSE 5000

CMD ["uvicorn", "app:app", "--reload", "--host", "0.0.0.0", "--port", "5000"]
