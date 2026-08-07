FROM python:3.11-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy pyproject.toml and lock file
COPY pyproject.toml uv.lock* ./

# Install dependencies
RUN uv sync

# Copy app
COPY . .

# Run app
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
