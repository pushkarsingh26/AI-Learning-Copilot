# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DATA_DIR=/app/data

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Ensure data directory exists and has appropriate permissions
RUN mkdir -p /app/data && chmod -R 777 /app/data

# Expose the default port for Streamlit/Hugging Face Spaces
EXPOSE 7860

# Command to start both FastAPI backend and Streamlit frontend
CMD ["sh", "-c", "uvicorn src.main:app --host 127.0.0.1 --port 8080 & streamlit run streamlit_app.py --server.port 7860 --server.address 0.0.0.0"]
