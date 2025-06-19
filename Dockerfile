FROM python:3.10-slim

# Set environment vars to avoid interactive prompts during build
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies needed by pip packages like cryptography and Firebase
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    libssl-dev \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements separately to cache Docker layers
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your app code
COPY . .

# Optional: Add a health check so Fly knows the app is ready
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s CMD curl --fail http://localhost:8080/ || exit 1

# Start your bot
CMD ["python", "main.py"]
