FROM node:22-slim AS frontend-dev

WORKDIR /app
COPY frontend/package*.json ./
RUN npm ci
EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]

FROM ghcr.io/astral-sh/uv:debian-slim AS backend-dev

RUN apt-get update && apt-get install -y --no-install-recommends \
    graphviz

WORKDIR /app

ENV UV_LINK_MODE=copy
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project


EXPOSE 8000
CMD ["uv", "run", "fastapi", "dev", "--host", "0.0.0.0"]
