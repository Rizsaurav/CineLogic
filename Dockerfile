# CineLogic: Autonomous AI Cinematography & Video Systems Engine
FROM python:3.11-slim

# Install system dependencies (FFmpeg & FFprobe required for video pipelines)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsm6 \
    libxext6 \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy dependency definitions and install
COPY requirements.txt pyproject.toml ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -e .

# Copy application files
COPY . .

# Ensure executable permissions on all entrypoints
RUN chmod +x mcp/*.py skills/cinelogic-cinematics/scripts/*.py tests/*.py examples/*.py

# Default entrypoint runs the full intensive test suite
CMD ["python3", "tests/run_intensive_tests.py"]
