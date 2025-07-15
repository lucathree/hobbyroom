FROM python:3.13.5-slim-bookworm AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0 \
    UV_PROJECT_ENVIRONMENT=/opt/.venv

WORKDIR /app

COPY . /app

RUN uv sync --frozen --no-dev --no-cache

ENV PATH="/opt/.venv/bin:$PATH"
