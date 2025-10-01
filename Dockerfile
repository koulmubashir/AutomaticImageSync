FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libgthread-2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY *.py ./
COPY *.md ./
COPY *.txt ./

# Create directories for data
RUN mkdir -p /app/input1 /app/input2 /app/output

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Create non-root user
RUN useradd -m -u 1000 imageuser && chown -R imageuser:imageuser /app
USER imageuser

# Default command (CLI version for Docker)
ENTRYPOINT ["python", "cli.py"]
CMD ["--help"]

# Labels
LABEL maintainer="your.email@example.com"
LABEL version="1.0.0"
LABEL description="Automatic Image Sync - Docker Edition"
