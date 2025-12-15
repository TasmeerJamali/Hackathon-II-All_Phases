# Backend Dockerfile
# Multi-stage build for FastAPI application

# Stage 1: Builder
FROM python:3.13-slim AS builder

WORKDIR /app

# Install UV
RUN pip install uv

# Copy dependency files
COPY pyproject.toml ./
COPY README.md ./

# Install dependencies
RUN uv sync --no-dev

# Stage 2: Runner
FROM python:3.13-slim AS runner

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY src/ ./src/

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app"

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

# Run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
