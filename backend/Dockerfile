FROM python:3.11-slim

# Minimal system deps for OpenCV headless + audio
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps first (cached layer)
COPY requirements.prod.txt .
RUN pip install --no-cache-dir -r requirements.prod.txt

COPY . .
RUN mkdir -p uploads/evidence

EXPOSE 8000

CMD gunicorn --bind 0.0.0.0:${PORT:-8000} --workers 2 --timeout 120 "app:create_app()"
