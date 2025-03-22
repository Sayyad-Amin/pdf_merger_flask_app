FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    poppler-utils \
    libmagic1 \
    ghostscript \
    tesseract-ocr \
    libreoffice \
    default-jre \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy project files
COPY . .

# Create directories for uploaded files and conversions
RUN mkdir -p uploads merged converted/word converted/jpg converted/excel converted/ppt

# Set permissions
RUN chmod -R 755 /app

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
