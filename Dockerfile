FROM python:3.11

WORKDIR /app

# Install system dependencies (for TensorFlow + PIL)
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for caching)
COPY backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy your code and model
COPY my_model/ ./my_model/
COPY backend/ ./backend/
COPY class_indices.json .
COPY main.py .

EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
