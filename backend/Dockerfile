FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Run database migrations
CMD alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8000 

# Install React type definitions
RUN cd frontend && npm install @types/react @types/react-dom 