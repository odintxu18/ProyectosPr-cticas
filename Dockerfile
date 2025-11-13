FROM python:3.13-slim
ENV STAGE=dev
WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY pyproject.toml /app
RUN uv sync --all-groups

COPY alembic.ini /app
COPY ./alembic /app/alembic
COPY ./src /app/src

RUN uv run alembic upgrade head

RUN apt-get update && apt-get install -y curl

EXPOSE 80




CMD ["uv", "run", "uvicorn", "src.api_main:main_app","--host", "0.0.0.0", "--port","80"]