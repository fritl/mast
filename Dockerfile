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
    --mount=type=bind,source=backend/uv.lock,target=uv.lock \
    --mount=type=bind,source=backend/pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project


EXPOSE 8000
CMD ["uv", "run", "fastapi", "dev", "--host", "0.0.0.0"]


FROM node:22-slim AS frontend-builder

WORKDIR /app
COPY frontend/package*.json ./
RUN npm ci
COPY ./frontend .
RUN npm run build



FROM ghcr.io/astral-sh/uv:debian-slim AS backend-builder

# Configure the Python directory so it is consistent
ENV UV_PYTHON_INSTALL_DIR=/python

# Only use the managed Python version
ENV UV_PYTHON_PREFERENCE=only-managed

ENV UV_LINK_MODE=copy
ENV UV_COMPILE_BYTECODE=1
# Install Python before the project for caching
RUN uv python install 3.14

WORKDIR /app
ENV UV_NO_DEV=1
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=backend/uv.lock,target=uv.lock \
    --mount=type=bind,source=backend/pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project
COPY  ./backend .
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked



FROM debian:trixie-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    graphviz
# Setup a non-root user
RUN groupadd --system --gid 999 nonroot \
 && useradd --system --gid 999 --uid 999 --create-home nonroot

# Copy the Python version
COPY --from=backend-builder /python /python

# Copy the application from the builder
COPY --from=backend-builder --chown=nonroot:nonroot /app /app

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

# Use the non-root user to run our application
USER nonroot

# Use `/app` as the working directory
WORKDIR /app
COPY --from=frontend-builder /app/dist dist/

# Run the FastAPI application by default
CMD ["fastapi", "run", "--host", "0.0.0.0", "--port", "8000"]
