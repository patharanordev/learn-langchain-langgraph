# ---- Builder stage ----
FROM python:3.13-slim AS builder

# Install required build tools for chroma-hnswlib (C++11)
RUN apt-get update && apt-get install -y build-essential

# Copy uv binary from official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
COPY --from=ghcr.io/astral-sh/uv:latest /uvx /bin/uvx

WORKDIR /app

COPY pyproject.toml uv.lock ./

# Sync dependencies (this will create `.venv`)
RUN uv venv && \
    . .venv/bin/activate && \
    uv sync --locked --no-install-project --no-editable

# ---- Runtime stage ----
FROM python:3.13-slim AS runner

# Add runtime dependencies if needed
RUN apt-get update && apt-get install -y libstdc++6

WORKDIR /app

COPY --from=builder ./app/.venv ./.venv
COPY . .

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["python", "main.py"]