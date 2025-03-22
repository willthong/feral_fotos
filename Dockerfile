FROM python:slim

ENV POETRY_VERSION=2.1.1 POETRY_VIRTUALENVS_CREATE=false

RUN pip install poetry==${POETRY_VERSION}
COPY pyproject.toml ./

RUN poetry install
COPY . ./

EXPOSE 8005
ENTRYPOINT ["gunicorn", "app:app"]
